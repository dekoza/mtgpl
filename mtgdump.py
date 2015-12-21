#!/usr/bin/env python2
#coding: utf-8
from mtglib.gatherer_request import SearchRequest
from mtglib.card_extractor import CardExtractor
from django.utils.encoding import smart_str
import re


def manarepl(match):
    d = match.groupdict()
    symbol = d['symbol'].replace('{', '').replace('}', '').replace('(', '').replace(')', '').replace('/', '')
    if symbol == 'T':
        return '|tap|'
    elif symbol == 'Q':
        return '|untap|'
    else:
        return '|mana_%s|' % symbol.lower()


sets = [
    ('Dragons of Tarkir', 'DTK'),
    ('Origins', 'ORI'),
    ('Battle for Zendikar', 'BFZ')
        ]
for s in sets:
#
    request = SearchRequest({'set': s[0]})
    cards = []
    oldcards = []
    for i in range(20):
        tmp = CardExtractor(request.url + "&page=%s" % i).cards
        if len(oldcards) > 0 and tmp[0].name == oldcards[0].name:
            break
        else:
            cards.extend(tmp)
            oldcards = tmp

            #~ with open("%s.pot" % s[1], 'wb') as dumpfile:
            #~ dumpfile.write("#. Please leave mana costs and tap symbol intact!\n")
            #~ for card in cards:
            #~ dumpfile.write("#: %s\n" % smart_str(card.name))
            #~ lines = smart_str(card.rules_text).replace(' ; ', ';').replace('"', r'\"').split(';')
            #~ for l in lines:
            #~ dumpfile.write('msgid "%s"\nmsgstr ""\n\n' % l)
            #~ dumpfile.write('\n')
        #~

    pat = re.compile(r'(?P<symbol>\{[WUBRGTXPQC]{1}\}|\{[0-9]+\}|\{\([2wubrg]{1}/[wubrgpc]{1}\)\})')

    with open("%s.rst" % s[1], 'wb') as dumpfile:
        dumpfile.write(".. %(name)s auto-download\n.. include:: symbols.rst\n\n%(name)s\n" % {'name': s[0]})
        dumpfile.write("".join(['=' for i in s[0]]) + '\n\n')
        for card in cards:
            dumpfile.write("%s\n" % smart_str(card.name))
            card_rules = smart_str(card.rules_text)
            card_rules = re.sub(pat, manarepl, card_rules)
            lines = card_rules.replace(' ; ', ';').replace('||', '| |').replace('"', r'\"').split(';')
            for l in lines:
                dumpfile.write('    %s\n\n' % l)
            dumpfile.write('\n')

