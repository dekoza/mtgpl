#!/usr/bin/env python2
#coding: utf-8
# from mtglib.gatherer_request import SearchRequest
# from mtglib.card_extractor import CardExtractor
from django.utils.encoding import smart_str

import os
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'mtgsalvation.settings') #Must be at the top before other imports

from scrapy import log, signals, project
from scrapy.xlib.pydispatch import dispatcher
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process, Queue

class CrawlerScript():
    def __init__(self):
        self.crawler = CrawlerProcess(settings)
        if not hasattr(project, 'crawler'):
            self.crawler.install()
        self.crawler.configure()
        self.items = []
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
        self.items.append(item)

    def crawl(self, queue, spider_name):
        spider = self.crawler.spiders.create(spider_name)
        # if spider:
        #     self.crawler.queue.append_spider(spider)
        # self.crawler.start()
        # self.crawler.stop()
        # queue.put(self.items)
        return spider.crawl()

    # def crawl(self, spider):
    #     queue = Queue()
    #     p = Process(target=self._crawl, args=(queue, spider,))
    #     p.start()
    #     p.join()
    #     return queue.get(True)

log.start()
cards = []
crawler = CrawlerScript()
cards.extend(crawler.crawl('mtgs'))

with open("THS.pot" , 'wb') as dumpfile:
    dumpfile.write("#. Please leave mana costs and tap symbol intact!\n")
    for card in cards:
        # print card
        dumpfile.write("#: %s\n" % smart_str(card['name'][0]))
        for l in card['text']:
            l = l.strip()
            l = smart_str(l).replace('"', r'\"')
            dumpfile.write('msgid "%s"\nmsgstr ""\n\n' % l)
        dumpfile.write('\n')
