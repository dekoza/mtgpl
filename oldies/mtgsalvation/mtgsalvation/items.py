# coding: utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MtgsalvationItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class CardItem(Item):
    name = Field()  # card name
    # cost = Field()  # mana cost
    # kind = Field()  # type(s)
    text = Field()  # text field


#    flav = Field()  # flavor text
#    ptl = Field()   # power/toughness/loyalty


class Cost(Item):
    cost = Field()
