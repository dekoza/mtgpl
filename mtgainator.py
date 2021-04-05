#!/usr/bin/env python3
from typing import TypedDict, Mapping, Optional

import typer
from decouple import config
from pathlib import Path
import shutil
import polib
import json
import hashlib
import os
import re
import zipfile
from datetime import date

from toolbox.mtg_vars import mtga_rev_map, mtga_cost_map

MTGA_DIR = config("MTGA_DIR")
SUBSTITUTE_LANG = config("SUBSTITUTE_LANG", default="pt-BR")
SUBSTITUTE_LANG_DEBUG = config("SUBSTITUTE_LANG_DEBUG", default="fr-FR")

assert "en-US" not in [
    SUBSTITUTE_LANG,
    SUBSTITUTE_LANG_DEBUG,
], "Dla własnego spokoju proszę nie usuwać angielskiego."

CURRENT_DIR = Path(__file__).absolute().parent
_main_lang = SUBSTITUTE_LANG.split("-")[0]
_debug_lang = SUBSTITUTE_LANG_DEBUG.split("-")[0]

app = typer.Typer()


def substr(text: str) -> str:
    trans_src = {
        "�": "'",
        "…": ".",
        "’": "'",
    }

    return text.translate({ord(k): ord(v) for k, v in trans_src.items()})


def get_valid_mtga_dl_path() -> Path:
    path = Path(MTGA_DIR)
    assert path.exists()
    assert path.is_dir()
    downloads = path / "Downloads"
    assert downloads.exists()
    assert downloads.is_dir()
    data_dir = downloads / "Data"
    loc_dir = downloads / "Loc"
    assert data_dir.exists()
    assert data_dir.is_dir()
    assert loc_dir.exists()
    assert loc_dir.is_dir()
    return downloads


def get_mtga_file(prefix: str, path: Path) -> Path:
    for i in os.listdir(path):
        if i.startswith(prefix) and i.endswith(".mtga"):
            return path / i


def extract_data_pots(path: Path):
    filename = get_mtga_file("data_loc", path)
    pot_path = CURRENT_DIR / "MTG" / "templates"

    po = polib.POFile()
    with open(path / filename) as infile:
        full_data = json.load(infile)
        data = get_en_trans(full_data)
        annotated = annotate_data_loc(data)
        with typer.progressbar(annotated.values(), label="Extracting Cards") as progress:
            for obj in progress:
                key = obj["id"]
                text = convert_mana_costs(obj["text"])
                entry = polib.POEntry(
                    msgctxt=str(key),
                    msgid=text,
                    msgstr="",
                    flags=list(obj.get("flags", []))
                )
                po.append(entry)
    po.save(f"{pot_path}/data_loc.pot")


class DataLoc(TypedDict):
    id: int
    text: int
    flags: Optional[set[str]]


def annotate_data_loc(data) -> Mapping[int, DataLoc]:
    annotated: dict[int, DataLoc] = {o["id"]: o for o in data}
    annotated.setdefault(0, {"id": 0, "text": ""})
    for o in annotated.values():
        o["flags"] = set()
    path = get_valid_mtga_dl_path()
    abilities_filepath = get_mtga_file("data_abilities", path / "Data")
    with open(abilities_filepath) as infile:
        abilities = json.load(infile)
    for ability in abilities:
        text_id = ability["text"]
        annotated[text_id]["flags"].add("internal ability")
    cards_filepath = get_mtga_file("data_cards", path / "Data")
    with open(cards_filepath) as infile:
        cards = json.load(infile)
    for card in cards:
        annotated[card["titleId"]]["flags"].add("card title")
        annotated[card["flavorId"]]["flags"].add("flavor text")
        annotated[card["cardTypeTextId"]]["flags"].add("card type")
        annotated[card["subtypeTextId"]]["flags"].add("card subtype")
    return annotated


def get_loc_en_trans(data, loc="en-US"):
    for i in data:
        if i["locale"] == loc:
            return i["translation"]


def extract_loc_pots(path: Path):
    pot_dir = CURRENT_DIR / "MTGA" / "t"
    mtga_files = (i for i in os.listdir(path) if i.endswith(".mtga"))

    with typer.progressbar(mtga_files, label="Extracting Game Locale") as progress:
        for filename in progress:
            po = polib.POFile()
            with open(path / filename) as infile:
                data = json.load(infile)
                for idx, obj in enumerate(data, start=1):
                    key = obj["key"]
                    bundle = obj["bundle"] or "Internal"
                    text = get_loc_en_trans(obj["translations"])
                    entry = polib.POEntry(
                        msgctxt=key,
                        msgid=text,
                        msgstr="",
                    )
                    po.append(entry)
            po.save(f"{pot_dir}/MTGA_{bundle}.pot")


def find_loc_idx(trans_list, lang="en-US"):
    for i, obj in enumerate(trans_list):
        if obj["locale"] == lang:
            return i


def find_loc_trans_obj(trans_list, lang="en-US"):
    for obj in trans_list:
        if obj["locale"] == lang:
            return obj


def create_datfile(filepath):
    with open(filepath, "rb") as done_file, open(f"{filepath}.dat", "w") as dat_file:
        dat_file.write("1\n")
        md5_hash = hashlib.md5()
        done_content = done_file.read()
        dat_file.write(f"{len(done_content)}\n")
        md5_hash.update(done_content)
        dat_file.write(f"{md5_hash.hexdigest()}\n")


def convert_mana_costs(string: str) -> str:
    energy_pat = r"(\{E+?\})"
    string = re.sub(energy_pat, convert_energy, string)
    loyalty_pat = r"(^-(\d+|X):)"
    string = re.sub(loyalty_pat, convert_loyalty, string)
    mana_pat = r"(\{o.+?\})"
    return re.sub(mana_pat, convert_mana, string)


def convert_loyalty(match) -> str:
    s = match.group()
    return s.replace("-", "–")


def convert_mana(match) -> str:
    s = match.group().strip("{o}")
    return r"\ ".join(mtga_cost_map[cost] for cost in s.split("o"))


def convert_energy(match) -> str:
    s = match.group().strip("{}")
    return r"\ ".join("|energy|" for i in range(len(s)))


def get_en_trans(data, loc="en-US"):
    for i in data:
        if i["isoCode"] == loc:
            return i["keys"]


def translate_data(path: Path):
    podir = CURRENT_DIR / "translated" / "pl" / "LC_MESSAGES"
    orig_path = path / "orig"

    mtga_files = (
        i for i in os.listdir(path) if i.startswith("data_loc") and i.endswith(".mtga")
    )
    pofiles = ["data_loc.po"]

    os.makedirs(orig_path, exist_ok=True)
    for filename in mtga_files:
        filepath = path / filename
        bak_filepath = orig_path / filename

        main_name = filename.rsplit("_", 1)[0]
        poname = f"{main_name}.po"
        if poname not in pofiles:
            continue

        if not bak_filepath.exists():
            shutil.move(filepath, bak_filepath)
            shutil.move(f"{filepath}.dat", f"{bak_filepath}.dat")

        with open(bak_filepath) as source, open(filepath, "w") as outfile:
            po = polib.pofile(podir / poname)
            data = json.load(source)

            do_the_trans(data, po, lang=SUBSTITUTE_LANG)
            do_the_trans(data, po, lang=SUBSTITUTE_LANG_DEBUG)

            json.dump(fp=outfile, obj=data, ensure_ascii=False, indent=2)

        create_datfile(filepath)


def translate_loc(path: Path):
    popath = CURRENT_DIR / "MTGA" / "trans" / "pl"
    orig_path = path / "orig"

    mtga_files = (i for i in os.listdir(path) if i.endswith(".mtga"))
    pofiles = [i for i in os.listdir(popath) if i.endswith(".po")]

    os.makedirs(orig_path, exist_ok=True)
    with typer.progressbar(mtga_files, label="Translating Game Binary") as progress:
        for filename in progress:
            filepath = path / filename
            bak_filepath = orig_path / filename
            bundle_name = filename.split("_", 1)[1].rsplit("_", 1)[0]
            poname = f"MTGA_{bundle_name}.po"

            if poname not in pofiles:
                continue

            if not bak_filepath.exists():
                shutil.move(filepath, bak_filepath)
                shutil.move(f"{filepath}.dat", f"{bak_filepath}.dat")

            with open(bak_filepath) as source, open(filepath, "w") as outfile:
                po = polib.pofile(popath / poname)
                data = json.load(source)
                for obj in data:
                    key = obj["key"]

                    po_entry = po.find(key, by="msgctxt")
                    trans_list = obj["translations"]

                    main_lang_key = f"MainNav/Settings/Debug/Language_{_main_lang}"
                    debug_lang_key = f"MainNav/Settings/Debug/Language_{_debug_lang}"

                    if key.startswith(main_lang_key):
                        for trans_obj in obj["translations"]:
                            trans_obj["translation"] = "Polski"

                    elif key.startswith(debug_lang_key):
                        for trans_obj in obj["translations"]:
                            trans_obj["translation"] = "Polski (DEBUG)"

                    elif po_entry:
                        trans_obj = find_loc_trans_obj(trans_list, lang=SUBSTITUTE_LANG)
                        trans_obj["translation"] = po_entry.msgstr or po_entry.msgid

                        debug_trans_obj = find_loc_trans_obj(
                            trans_list, lang=SUBSTITUTE_LANG_DEBUG
                        )
                        debug_trans_obj["translation"] = po_entry.msgstr or key

                    else:
                        pass

                json.dump(fp=outfile, obj=data, ensure_ascii=False, indent=2)
            create_datfile(filepath)


@app.command(name="e", hidden=True)
@app.command(name="extract")
def extract_pots():
    path = get_valid_mtga_dl_path()
    extract_loc_pots(path / "Loc")
    extract_data_pots(path / "Data")
    typer.echo("Done!")


@app.command(name="t", hidden=True)
@app.command(name="trans", hidden=True)
@app.command()
def translate():
    path = get_valid_mtga_dl_path()
    translate_loc(path / "Loc")
    translate_data(path / "Data")
    typer.echo("Done!")


@app.command(name="b", hidden=True)
@app.command()
def build():
    path = get_valid_mtga_dl_path()
    dist_path = CURRENT_DIR / "_mtga_dist"
    os.makedirs(dist_path, exist_ok=True)

    loc_path = path / "Loc"
    data_path = path / "Data"

    dt = date.today()

    date_part = dt.strftime("%Y.%m.%d")
    release = 1
    while (
            filename := (dist_path / f"MTGA_Data-{date_part}.{release:02d}.zip")
    ).exists():
        release += 1

    add_tag_to_dat_files(path, version=f"{date_part}.{release:02d}")

    with zipfile.ZipFile(
            filename, "w", compression=zipfile.ZIP_BZIP2, compresslevel=9
    ) as archive:
        for filename in (i for i in os.listdir(data_path) if i.startswith("data_loc_")):
            archive.write(
                data_path / filename, arcname=f"MTGA_Data/Downloads/Data/{filename}"
            )
        for filename in (i for i in os.listdir(loc_path) if i.startswith("loc_")):
            archive.write(
                loc_path / filename, arcname=f"MTGA_Data/Downloads/Loc/{filename}"
            )

    typer.echo("Done!")


def tag_dats_in_path(filelist, path, version):
    for filename in filelist:
        with open(path / filename, "a") as datfile:
            datfile.write(f"\nmtgapl:{version}\n")


def add_tag_to_dat_files(path, version=""):
    loc_path = path / "Loc"
    data_path = path / "Data"
    loc_files = (
        i for i in os.listdir(loc_path) if i.startswith("loc_") and i.endswith(".dat")
    )
    data_files = (
        i
        for i in os.listdir(data_path)
        if i.startswith("data_loc_") and i.endswith(".dat")
    )
    tag_dats_in_path(loc_files, loc_path, version)
    tag_dats_in_path(data_files, data_path, version)


def find_data_trans_obj(trans_list, lang="en-US"):
    for obj in trans_list:
        if obj["isoCode"] == lang:
            return obj


def revert_costs(string: str) -> str:
    energy_pat = r"(\|energy(\|\\.)*)+\|"
    string = re.sub(energy_pat, restore_energy, string)
    loyalty_pat = r"(^–(\d+|X):)"
    string = re.sub(loyalty_pat, restore_loyalty, string)
    mana_pat = r"(\|(mana_[wubrgspx\d]+|colorless|(un)?tap)(\|\\.)*)+\|"
    return re.sub(mana_pat, restore_mana, string)


def restore_energy(match) -> str:
    s = match.group().split(r"\ ")
    try:
        return "{%s}" % "".join(mtga_rev_map[cost] for cost in s)
    except KeyError:
        print(match.string)
        print(s)
        raise


def restore_mana(match) -> str:
    s = match.group().split(r"\ ")
    try:
        return "{%s}" % "".join(f"o{mtga_rev_map[cost]}" for cost in s)
    except KeyError:
        print(match.string)
        print(s)
        raise


def restore_loyalty(match) -> str:
    s = match.group()
    return s.replace("–", "-")


def do_the_trans(data, pofile, lang="en-US"):
    translation_objs = find_data_trans_obj(data, lang=lang)["keys"]

    with typer.progressbar(
            translation_objs, label=f"Substituting cards for {lang}"
    ) as progress:
        for obj in progress:
            obj_id = str(obj["id"])
            po_entry = pofile.find(obj_id, by="msgctxt")
            if po_entry:
                if po_entry.fuzzy:
                    text = revert_costs(po_entry.msgid)
                else:
                    text = revert_costs(po_entry.msgstr or po_entry.msgid)
                obj["text"] = text


if __name__ == "__main__":
    app()
