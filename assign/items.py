# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class AssignItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # URL of blog
    url = Field()

    # heading of the blog
    header = Field()

    #title of the blog
    title = Field()

    # description of the blog
    desc = Field()

    # images if any with the blog
    image = Field()

    # vote count of the blog
    vote = Field()
    