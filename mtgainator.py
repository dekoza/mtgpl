#!/usr/bin/env python3
import typer
from decouple import config
import pathlib
import shutil
import polib
import json
import hashlib
import os

MTGA_DIR = config("MTGA_DIR")
SUBSTITUTE_LANG = config("SUBSTITUTE_LANG", default="pt-BR")
SUBSTITUTE_LANG_DEBUG = config("SUBSTITUTE_LANG_DEBUG", default="fr-FR")

assert "en-US" not in [SUBSTITUTE_LANG, SUBSTITUTE_LANG_DEBUG], "Proszę nie usuwać oryginalnego tłumaczenia."

CURRENT_DIR = pathlib.Path(__file__).absolute().parent
_main_lang = SUBSTITUTE_LANG.split("-")[0]
_debug_lang = SUBSTITUTE_LANG_DEBUG.split("-")[0]

app = typer.Typer()


def substr(text: str) -> str:
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


def extract_data_pots():
    pass

def get_loc_en_trans(l, loc="en-US"):
    for i in l:
        if i["locale"] == loc:
            return i["translation"]

def extract_loc_pots(path:pathlib.Path):
    pot_dir = CURRENT_DIR / "MTGA" / "t"
    mtga_files = (i for i in os.listdir(path) if i.endswith(".mtga"))

    with typer.progressbar(mtga_files, label="Extracting LOC")
        for filename in mtga_files:
            po = polib.POFile()
            with open(filename) as infile:
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


def translate_data(path: pathlib.Path):
    pass


def translate_loc(path: pathlib.Path):
    popath = CURRENT_DIR / "MTGA" / "trans" / "pl"
    orig_path = path / "orig"

    mtga_files = (i for i in os.listdir(path) if i.endswith(".mtga"))
    pofiles = [i for i in os.listdir(popath) if i.endswith(".po")]

    os.makedirs(orig_path, exist_ok=True)
    with typer.progressbar(mtga_files, label="Translating LOC") as progress:
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
                            po_entry.msgstr or po_entry.msgid
                        )

                        debug_trans_obj = find_loc_trans_obj(
                            trans_list, lang=SUBSTITUTE_LANG_DEBUG
                        )
                        debug_trans_obj["translation"] = substr(po_entry.msgstr or key)
                    else:
                        raise ZeroDivisionError

                json.dump(fp=outfile, obj=data, ensure_ascii=False, indent=2)
            create_datfile(filepath)


@app.command(name="e", hidden=True)
@app.command(name="extract")
def extract_pots():
    path = get_valid_mtga_dl_path()
    extract_loc_pots()
    extract_data_pots()


@app.command(name="t", hidden=True)
@app.command(name="trans", hidden=True)
@app.command()
def translate():
    path = get_valid_mtga_dl_path()
    translate_loc(path / "Loc")
    translate_data(path / "Data")


@app.command(name="b", hidden=True)
@app.command()
def build():
    path = get_valid_mtga_dl_path()
    # copy original files to tempdir
    # prepare zipfile with translations for distribution
    # save zipfile in `build` dir with proper name
    pass


if __name__ == "__main__":
    app()
