#coding: utf-8
import re

exp = r'^(?P<numer>\d{3}\.\d+[a-z.]*) (?P<content>.+)'

result = []

with open('comprules.rst','r') as plik:
    for line in plik.xreadlines():
        r = re.match(exp, line)
        if r:
            number, content = r.groups()
            number = number.strip('.')
            result.append(number+'\n')
            result.append('-'*len(number)+'\n')
            result.append(content+'\n')
        else:
            result.append(line)
with open('cmpformat.rst','w') as zapis:
    zapis.writelines(result)

