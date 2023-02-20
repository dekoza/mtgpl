#!/usr/bin/env python3

import os
import pathlib

import polib

CURRENT_DIR = pathlib.Path(__file__).parent
trans_dir = CURRENT_DIR / "translated/pl/LC_MESSAGES"

mtg_exps = (f for f in os.listdir(trans_dir) if f.endswith(".po") and len(f) in {6, 7})


def percent_translated(obj):
    total = len([e for e in obj if not e.obsolete and not e.msgid.startswith(":")])
    if total == 0:
        return 100
    translated = len(obj.translated_entries())
    return int(translated * 100 / float(total))


with open("percentages.inc", "w") as outfile:
    for filename in mtg_exps:
        expansion = filename.split(".")[0]
        pofile = polib.pofile(trans_dir / filename)
        percentage = (percent_translated(pofile) // 5 * 5) or 5
        pie = f"pie{percentage:02d}" if percentage < 100 else "done"
        outfile.write(
            f"""
.. |{expansion}_percent| image:: images/{pie}.png        
"""
        )
        if percentage == 100:
            outfile.write("   :alt: Tłumaczenie zakończone\n")
