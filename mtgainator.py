#!/usr/bin/env python3
import typer
from decouple import config
import pathlib
import shutil
import polib
import json
import hashlib
import os
import re
import zipfile
from datetime import date

MTGA_DIR = config("MTGA_DIR")
SUBSTITUTE_LANG = config("SUBSTITUTE_LANG", default="pt-BR")
SUBSTITUTE_LANG_DEBUG = config("SUBSTITUTE_LANG_DEBUG", default="fr-FR")

assert "en-US" not in [
    SUBSTITUTE_LANG,
    SUBSTITUTE_LANG_DEBUG,
], "Proszę nie usuwać oryginalnego tłumaczenia."

CURRENT_DIR = pathlib.Path(__file__).absolute().parent
_main_lang = SUBSTITUTE_LANG.split("-")[0]
_debug_lang = SUBSTITUTE_LANG_DEBUG.split("-")[0]

app = typer.Typer()
rev_map = {
    "|energy|": "E",
    "|colorless|": "C",
    "|tap|": "T",
    "|untap|": "Q",
    "|mana_u|": "U",
    "|mana_w|": "W",
    "|mana_g|": "G",
    "|mana_b|": "B",
    "|mana_r|": "R",
    "|mana_p|": "P",
    "|mana_s|": "Si",
    "|mana_2u|": "(2/U)",
    "|mana_2w|": "(2/W)",
    "|mana_2b|": "(2/B)",
    "|mana_2g|": "(2/G)",
    "|mana_2r|": "(2/R)",
    "|mana_up|": "(U/P)",
    "|mana_wp|": "(W/P)",
    "|mana_bp|": "(B/P)",
    "|mana_gp|": "(G/P)",
    "|mana_rp|": "(R/P)",
    "|mana_x|": "X",
    "|mana_0|": "0",
    "|mana_1|": "1",
    "|mana_2|": "2",
    "|mana_3|": "3",
    "|mana_4|": "4",
    "|mana_5|": "5",
    "|mana_6|": "6",
    "|mana_7|": "7",
    "|mana_8|": "8",
    "|mana_9|": "9",
    "|mana_10|": "10",
    "|mana_11|": "11",
    "|mana_12|": "12",
    "|mana_13|": "13",
    "|mana_14|": "14",
    "|mana_15|": "15",
    "|mana_rg|": "(R/G)",
    "|mana_rw|": "(R/W)",
    "|mana_ub|": "(U/B)",
    "|mana_ur|": "(U/R)",
    "|mana_wb|": "(W/B)",
    "|mana_wu|": "(W/U)",
    "|mana_bg|": "(B/G)",
    "|mana_br|": "(B/R)",
    "|mana_gw|": "(G/W)",
    "|mana_gu|": "(G/U)",
}

cost_map = {
    "C": "|colorless|",
    "T": "|tap|",
    "Q": "|untap|",
    "U": "|mana_u|",
    "W": "|mana_w|",
    "G": "|mana_g|",
    "B": "|mana_b|",
    "R": "|mana_r|",
    "P": "|mana_p|",
    "Si": "|mana_s|",
    "(2/U)": "|mana_2u|",
    "(2/W)": "|mana_2w|",
    "(2/B)": "|mana_2b|",
    "(2/G)": "|mana_2g|",
    "(2/R)": "|mana_2r|",
    "(U/P)": "|mana_up|",
    "(W/P)": "|mana_wp|",
    "(B/P)": "|mana_bp|",
    "(G/P)": "|mana_gp|",
    "(R/P)": "|mana_rp|",
    "X": "|mana_x|",
    "0": "|mana_0|",
    "1": "|mana_1|",
    "2": "|mana_2|",
    "3": "|mana_3|",
    "4": "|mana_4|",
    "5": "|mana_5|",
    "6": "|mana_6|",
    "7": "|mana_7|",
    "8": "|mana_8|",
    "9": "|mana_9|",
    "10": "|mana_10|",
    "11": "|mana_11|",
    "12": "|mana_12|",
    "13": "|mana_13|",
    "14": "|mana_14|",
    "15": "|mana_15|",
    "(R/G)": "|mana_rg|",
    "(R/W)": "|mana_rw|",
    "(U/B)": "|mana_ub|",
    "(U/R)": "|mana_ur|",
    "(W/B)": "|mana_wb|",
    "(W/U)": "|mana_wu|",
    "(B/G)": "|mana_bg|",
    "(B/R)": "|mana_br|",
    "(G/W)": "|mana_gw|",
    "(G/U)": "|mana_gu|",
}


def substr(text: str, use_alt: bool = False) -> str:
    if use_alt:
        trans_src = {
            "ą": "á",
            "Ą": "Á",
            "ć": "c",
            "ę": "é",
            "Ę": "É",
            "Ł": "L",
            "Ń": "Ñ",
            "ś": "š",
            "Ś": "Š",
            "ź": "ž",
            "Ź": "Ž",
            "ż": "ž",
            "Ż": "Ž",
        }
    else:
        trans_src = {
            "ą": "a",
            "Ą": "A",
            "ć": "c",
            "ę": "e",
            "Ę": "E",
            "Ł": "L",
            "Ń": "N",
            "ś": "s",
            "Ś": "S",
            "ź": "z",
            "Ź": "Z",
            "ż": "z",
            "Ż": "Z",
        }

    return text.translate({ord(k): ord(v) for k, v in trans_src.items()})


def get_valid_mtga_dl_path() -> pathlib.Path:
    path = pathlib.Path(MTGA_DIR)
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


def extract_data_pots(path: pathlib.Path):
    mtga_files = (
        i for i in os.listdir(path) if i.startswith("data_loc_") and i.endswith(".mtga")
    )
    pot_path = CURRENT_DIR / "MTG" / "templates"

    po = polib.POFile()
    for filename in mtga_files:
        with open(path / filename) as infile:
            full_data = json.load(infile)
            data = get_en_trans(full_data)
            with typer.progressbar(data, label="Extracting Cards") as progress:
                for obj in progress:
                    key = obj["id"]
                    text = convert_mana_costs(obj["text"])
                    entry = polib.POEntry(
                        msgctxt=str(key),
                        msgid=text,
                        msgstr="",
                    )
                    po.append(entry)
    po.save(f"{pot_path}/data_loc.pot")


def get_loc_en_trans(data, loc="en-US"):
    for i in data:
        if i["locale"] == loc:
            return i["translation"]


def extract_loc_pots(path: pathlib.Path):
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
    return r"\ ".join(cost_map[cost] for cost in s.split("o"))


def convert_energy(match) -> str:
    s = match.group().strip("{}")
    return r"\ ".join("|energy|" for i in range(len(s)))


def get_en_trans(data, loc="en-US"):
    for i in data:
        if i["isoCode"] == loc:
            return i["keys"]


def translate_data(path: pathlib.Path, use_alt: bool = False):
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

            do_the_trans(data, po, lang=SUBSTITUTE_LANG, use_alt=use_alt)
            do_the_trans(data, po, lang=SUBSTITUTE_LANG_DEBUG, use_alt=use_alt)

            json.dump(fp=outfile, obj=data, ensure_ascii=False, indent=2)

        create_datfile(filepath)


def translate_loc(path: pathlib.Path, use_alt: bool = False):
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
                            trans_obj["translation"] = "Polski+English"

                    elif key.startswith(debug_lang_key):
                        for trans_obj in obj["translations"]:
                            trans_obj["translation"] = "Pl+En (DEBUG)"

                    elif po_entry:
                        trans_obj = find_loc_trans_obj(trans_list, lang=SUBSTITUTE_LANG)
                        trans_obj["translation"] = substr(
                            po_entry.msgstr or po_entry.msgid, use_alt=use_alt
                        )

                        debug_trans_obj = find_loc_trans_obj(
                            trans_list, lang=SUBSTITUTE_LANG_DEBUG
                        )
                        debug_trans_obj["translation"] = substr(
                            po_entry.msgstr or key, use_alt=use_alt
                        )
                    else:
                        raise ZeroDivisionError

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
def translate(
    alt: bool = typer.Option(False, help="Podmień polskie znaki na inne specjalne. Przynajmniej będą się bardziej wyróżniać ;)")
):
    path = get_valid_mtga_dl_path()
    translate_loc(path / "Loc", use_alt=alt)
    translate_data(path / "Data", use_alt=alt)
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
    while (filename := (dist_path / f"MTGA_Data-{date_part}.{release:02d}.zip")).exists():
        release += 1

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
        return "{%s}" % "".join(rev_map[cost] for cost in s)
    except KeyError:
        print(match.string)
        print(s)
        raise


def restore_mana(match) -> str:
    s = match.group().split(r"\ ")
    try:
        return "{%s}" % "".join(f"o{rev_map[cost]}" for cost in s)
    except KeyError:
        print(match.string)
        print(s)
        raise


def restore_loyalty(match) -> str:
    s = match.group()
    return s.replace("–", "-")


def do_the_trans(data, pofile, lang="en-US", use_alt: bool = False):
    translation_objs = find_data_trans_obj(data, lang=lang)["keys"]

    with typer.progressbar(
        translation_objs, label=f"Substituting cards for {lang}"
    ) as progress:
        for obj in progress:
            obj_id = str(obj["id"])
            po_entry = pofile.find(obj_id, by="msgctxt")
            if po_entry:
                text = revert_costs(po_entry.msgstr or po_entry.msgid)
                obj["text"] = substr(text, use_alt=use_alt)


if __name__ == "__main__":
    app()
