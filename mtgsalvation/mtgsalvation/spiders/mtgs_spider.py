#coding: utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from mtgsalvation.items import CardItem


def normalize_mana_cost(text):
    import re
    pat = re.compile(r'<img.*?alt=["|\'](?P<alt>.*?)["|\'].*?[/]?>')
    return re.sub(pat, "\g<alt>", text)


class MTGSalvationCrawler(BaseSpider):
    name = 'mtgs'
    allowed_domains = ['gatheringmagic.com']
    start_urls = ['http://www.gatheringmagic.com/magic-the-gathering-sets/theros-spoilers/']

    def parse(self, response):
        x = HtmlXPathSelector(response)
        cards = []
        for item in x.select("//div[contains(@class,'spoiler-card')]"):
            card = CardItem() 
            card['name'] = item.select('.//span[contains(@class,"title")]/a[last()]/text()').extract()
            tmp = item.select('.//div[contains(@class,"text")][last()]').extract()
            if len(tmp) > 0:
                tmp = normalize_mana_cost(tmp[0])
                nx = HtmlXPathSelector(text=tmp)
                card['text'] = nx.select('//text()').extract()
            else:
                card['text'] = ''
            cards.append(card)
        return cards

