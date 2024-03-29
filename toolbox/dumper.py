import asyncio
import os
import shutil
import tempfile
from collections import defaultdict
from typing import Iterable

import anyio
import appdirs
import httpx
import orjson
import pendulum
import trio
from anyio import Path, open_file

from toolbox.mtg_vars import card_template, missing_cards, symbols_map

data_save_path = Path(appdirs.user_data_dir("pl.mtgpopolsku.mtgd"))
bulk_file_path = data_save_path / "bulk.json"
check_file_path = data_save_path / "last_download.txt"


async def get_bulk_data(client: httpx.AsyncClient, bulk_type: str):
    url = "https://api.scryfall.com/bulk-data"
    await data_save_path.mkdir(exist_ok=True)

    last_download = pendulum.datetime(1970, 1, 1, 0, 0, 1)
    if await check_file_path.exists():
        async with await open_file(check_file_path, "r") as check_file:
            last_download = pendulum.parse(await check_file.read())

    fd, path = tempfile.mkstemp()
    async with client, await open_file(fd, "bw") as output:
        bulk_info = await client.get(url)
        if bulk_info.status_code != 200:
            raise httpx.ConnectError(
                f"Error fetching bulk data! {bulk_info.status_code}"
            )
        bulk_map = {b["type"]: b for b in bulk_info.json()["data"]}
        bulk_obj = bulk_map[bulk_type]
        updated_at = pendulum.parse(bulk_obj["updated_at"])
        if not await bulk_file_path.exists() or updated_at <= last_download:
            print("Nothing changed")
            return

        bulk_url = bulk_obj["download_uri"]

        async with client.stream("GET", bulk_url) as response:
            async for chunk in response.aiter_bytes():
                await output.write(chunk)
    shutil.copy(path, bulk_file_path)
    async with await open_file(check_file_path, "w") as check_file:
        await check_file.write(str(pendulum.now("UTC")))
    os.remove(path)


async def render_wanted(client: httpx.AsyncClient, use_bulk: bool = False):
    url_template = "https://api.scryfall.com/cards/{expansion}/{number}"
    url_cleanse = "https://www.cardmarket.com/en/Magic/Products/Singles/Legends/Cleanse"
    fd, path = tempfile.mkstemp(text=True)

    async with await open_file(fd, "w") as output, client:
        await output.write("Poszukiwane karty\n=================\n")
        for title, links in missing_cards.items():
            await output.write(f"\n{title}\n{len(title) * '-'}\n\n")
            mapped = defaultdict(list)
            for link in links:
                expansion, number = link.split("/")[4:6]
                mapped[expansion].append(number)

            for expansion, numbers in mapped.items():
                for number in numbers:
                    card = await client.get(url_template.format(**locals()))
                    c = card.json()
                    card_url = c.get("purchase_uris", {}).get("cardmarket") or url_cleanse
                    await output.write(
                        f".. image:: {c['image_uris']['small']}\n"
                        f"   :target: {card_url}\n"
                    )
    shutil.copy(path, f"poszukiwane.rst")
    os.remove(path)


async def queue_downloads(exp_list: Iterable, client, use_bulk):
    async with trio.open_nursery() as nursery:
        for exp in exp_list:
            nursery.start_soon(download_expansion, exp, client, use_bulk)


async def get_set_name(exp, client):
    result = await client.get(f"https://api.scryfall.com/sets/{exp.lower()}")
    if result.status_code != 200:
        raise httpx.ConnectError(f"Got error getting {exp} info: {result.status_code}")
    return result.json()["name"]


async def get_set_from_bulk(exp):
    exp = exp.lower()
    if not await bulk_file_path.exists():
        raise AssertionError("Bulk not found!")
    async with await open_file(bulk_file_path, "r") as data_file:
        all_cards = orjson.loads(await data_file.read())
    exp_cards = (c for c in all_cards if c["set"] == exp)
    return sorted(exp_cards, key=lambda c: int(c["collector_number"]))


async def get_set_cards(exp, client, use_bulk: bool = False):
    if use_bulk:
        return await get_set_from_bulk(exp)

    while result := await client.get(
            f"https://api.scryfall.com/cards/search?order=set&q=e%3A{exp.lower()}&unique=prints",
    ):
        if result.status_code != 200:
            if result.status_code == 429:
                print(f"waiting on {exp}")
                await anyio.sleep(63)
                continue
            else:
                raise httpx.ConnectError(
                    f"Got error getting {exp} card list: {result.status_code}"
                )
        break
    data = result.json()
    cards: list = data["data"]
    while data["has_more"]:
        while result := await client.get(data["next_page"]):
            if result.status_code != 200:
                if result.status_code == 429:
                    await anyio.sleep(63)
                    print(f"waiting on {exp}, next page")
                    continue
                else:
                    raise httpx.ConnectError(
                        f"Got error getting {exp} card list: {result.status_code}"
                    )
            break
        data = result.json()
        cards.extend(data["data"])
    return cards


async def write_file_header(exp, name, file):
    await file.write(
        f".. {name} (autogenerated)\n"
        ".. include:: symbols.rst\n\n"
        f":mtgexp:`{exp}` {name}\n"
        f"{(len(name) + len(exp) + 12) * '='}\n\n"
    )


async def write_card_data(cards, file):
    cache = []
    for card in cards:
        if (card_name := card["name"]) not in cache:
            cache.append(card_name)
            await write_single_card(card, file)


async def write_single_card(card, file):
    faces = card.get("card_faces", [card])
    for face in faces:
        if "image_uris" in face:
            image_uri = face["image_uris"]["border_crop"]
        else:
            image_uri = card["image_uris"]["border_crop"]
        await file.write(
            card_template.format(
                card=face,
                card_uri=card["scryfall_uri"],
                image=image_uri,
                card_text=reformat_card_text(face.get("oracle_text", "")),
            )
        )


async def download_expansion(exp: str, client: httpx.AsyncClient, use_bulk=False):
    fd, path = tempfile.mkstemp(text=True)

    async with await open_file(fd, "w") as output:
        # TODO: get only existing sets

        name = await get_set_name(exp, client)
        data = await get_set_cards(exp, client, use_bulk)
        await write_file_header(exp, name, output)
        await write_card_data(data, output)

    shutil.copy(path, f"{exp}.rst")
    os.remove(path)


def reformat_card_text(text, card_name=None):
    for t, s in symbols_map.items():
        text = text.replace(t, s)
    return text
