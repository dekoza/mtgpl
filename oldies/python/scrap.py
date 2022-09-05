# coding: utf-8

from scrapy.item import Field, Item
from scrapy.spider import BaseSpider


class CardItem(Item):
    name = Field()  # card name
    cost = Field()  # mana cost
    kind = Field()  # type(s)
    text = Field()  # text field
    flav = Field()  # flavor text
    ptl = Field()  # power/toughness/loyalty


class MTGSalvationCrawler(BaseSpider):
    name = "mtgsalvation.com"
    allowed_domains = ["mtgsalvation.com"]
    start_urls = ["http://www.mtgsalvation.com/theros-spoiler.html"]

    def parse(self, response):
        x = HtmlXPathSelector(response)
        cards = []
        for item in x.select("//table//table//table//tr/td")[5:]:
            card = CardItem()
            card["name"] = item.select(".//h3/a/text()").extract()
            card["cost"] = "-".join(t.select(".//td/img/@alt").extract()[:-1])
            card["kind"] = t.select(".//tr//td[@width]").extract()[-2]
            card["text"] = "\n".join(
                [i.strip() for i in t.select(".//tr//td[@colspan]/text()").extract()]
            )
            #            card['flav']
            #            card['ptl']
            cards.append(card)
        return cards
