import os
import shutil
import tempfile
from typing import Iterable
from rich.live import Live
from rich.table import Table
import httpx
import trio

from toolbox.mtg_vars import card_template, symbols_map


class DumperProgress(trio.abc.Instrument):
    pass


async def queue_downloads(exp_list: Iterable):
    async with trio.open_nursery() as nursery:
        for exp in exp_list:
            nursery.start_soon(download_expansion, exp)


async def download_expansion(exp: str):
    cache = []
    fd, path = tempfile.mkstemp(text=True)
    with open(fd, "w") as output:
        async with httpx.AsyncClient(timeout=15) as client:
            result = await client.get(f"https://api.scryfall.com/sets/{exp.lower()}")
            if result.status_code != 200:
                return
            name = result.json()["name"]
            result = await client.get(
                f"https://api.scryfall.com/cards/search?order=set&q=e%3A{exp.lower()}&unique=prints",
            )
            if result.status_code != 200:
                return
            data = result.json()
            output.write(
                f""".. {name} (autogenerated)
.. include:: symbols.rst

:mtgexp:`{exp}` {name}
{(len(name) + len(exp) + 12) * '='}

"""
            )
            while True:
                for card in data["data"]:
                    name = card["name"]
                    if name not in cache:
                        cache.append(name)
                        if card.get("card_faces"):
                            for face in card["card_faces"]:
                                if "image_uris" in face:
                                    image_uri = face["image_uris"]["border_crop"]
                                else:
                                    image_uri = card["image_uris"]["border_crop"]
                                output.write(
                                    card_template.format(
                                        card=face,
                                        card_uri=card["scryfall_uri"],
                                        image=image_uri,
                                        card_text=reformat_card_text(
                                            face.get("oracle_text", "")
                                        ),
                                    )
                                )
                        else:
                            output.write(
                                card_template.format(
                                    card=card,
                                    card_uri=card["scryfall_uri"],
                                    image=card["image_uris"]["border_crop"],
                                    card_text=reformat_card_text(
                                        card.get("oracle_text", "")
                                    ),
                                )
                            )
                if not data["has_more"]:
                    break
                result = await client.get(data["next_page"])
                data = result.json()
    shutil.copy(path, f"{exp}.rst")
    os.remove(path)


def reformat_card_text(text, card_name=None):
    for t, s in symbols_map.items():
        text = text.replace(t, s)
    # if card_name is not None:
    #     text = text.replace(card_name, 'this card')
    return text
