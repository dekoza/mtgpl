#!/usr/bin/env python2
#coding: utf-8
from mtglib.gatherer_request import SearchRequest
from mtglib.card_extractor import CardExtractor
from django.utils.encoding import smart_str

#~ sets = [('Return to Ravnica', 'RTR'), ('Gatecrash', 'GTC'), ("Dragon's Maze", 'DGM'), ('Magic 2014 Core Set', 'M14')]
#sets = [('Theros', 'THS'),]
sets = [('Commander 2013', 'C13'),]
for s in sets:
#
    request = SearchRequest({'set': s[0]})
    cards = []
    oldcards = []
    for i in range(20):
        tmp = CardExtractor(request.url + "&page=%s"%i).cards
        if len(oldcards) > 0 and tmp[0].name == oldcards[0].name:
            break
        else:
            cards.extend(tmp)
            oldcards = tmp

    with open("%s.pot" % s[1], 'wb') as dumpfile:
        dumpfile.write("#. Please leave mana costs and tap symbol intact!\n")
        for card in cards:
            dumpfile.write("#: %s\n" % smart_str(card.name))
            lines = smart_str(card.rules_text).replace(' ; ', ';').replace('"', r'\"').split(';')
            for l in lines:
                dumpfile.write('msgid "%s"\nmsgstr ""\n\n' % l)
            dumpfile.write('\n')
