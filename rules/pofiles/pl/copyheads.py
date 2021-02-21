# coding: utf-8

import re

exp = r'^(?P<numer>msgid "\d{3}\..*)$'

result = []
first = True
with open("./comprules.po", "r") as plik:
    for line in plik.xreadlines():
        r = re.match(exp, line)
        if r:
            result.append(line)
            result.append(line.replace("msgid", "msgstr"))
            first = False
        elif first:
            result.append(line)
        else:
            first = True

with open("./cmprls.po", "w") as zapis:
    zapis.writelines(result)
