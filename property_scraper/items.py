# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy import Field, Item
from scrapy.loader.processors import MapCompose, TakeFirst, Join

def remove_nt(value):
    return value.replace("\n", ' ').replace(" ", "")

def filter_num(value):
    if value.isalnum():
        return value[0]
    else:
        return "8"

def remove_text(value):
    return re.sub("[^0-9]", "", value)


class PxItem(scrapy.Item):

    href = scrapy.Field() # property page link.
    price = scrapy.Field(
        input_processor = MapCompose(str.strip, remove_nt),
        output_processor = TakeFirst()
    ) # property price

    location = scrapy.Field()  # Property location
    title = scrapy.Field() # Description about property
    type = scrapy.Field() # Porperty type

    bedrooms = scrapy.Field(
        default=0,
        input_processor=MapCompose(str.strip, filter_num),
        output_processor=TakeFirst()
    ) # Total Bedrooms property consists

    bathrooms = scrapy.Field(
        default=0,
        input_processor=MapCompose(str.strip, filter_num),
        output_processor=TakeFirst()
    ) # Total Bathrooms property consists

    floor_area = scrapy.Field(
        default=0,
        input_processor=MapCompose(str.strip, filter_num),
        output_processor=TakeFirst()
    ) # Total floor area / Carpet Area of property

    latitude = scrapy.Field() # Property Latitudes
    longitude = scrapy.Field() # Property longitude
    listing_url = scrapy.Field() # Url of property page



