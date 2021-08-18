import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from items import PxItem
from urllib.parse import urljoin, urlencode


class PropertyFinder(scrapy.Spider):

    # scraper name
    name = "property"

    # custom setting
    custom_settings = {'FEED_FORMAT': 'csv', 'FEED_URI': 'propertyfinder.csv'}

    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }


    def start_requests(self):
        # Starting url
        url = "https://www.propertyfinder.bh/en/search?c=1&ob=mr&page=1"
        # Crawl next page url
        yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        for card in response.xpath("//div[@class='card-list__item']"):

            # Create item loader object
            lst = ItemLoader(item=PxItem(), selector = card, response=response)

            # Convert link to URL
            domain = 'https://www.propertyfinder.bh'
            relative_url = card.xpath(".//a[@class= 'card card--clickable']/@href").get()
            url = urljoin(domain, relative_url)
            # print(url)

            # Attempt to extract Geo-coordinates Locations
            try:
                script = json.loads(json.dumps(response.xpath("//script[@type = 'application/ld+json']/text()").extract()))

                # Loop over the JSON card to get geo-coordinates
                for card in script[0]['itemListElement']:
                    if url == card['url']:
                        # Add Longitude & Latitude
                        lst.add_value('longitude', card['mainEntity']["geo"]["longitude"])
                        lst.add_value('latitude', card['mainEntity']["geo"]["latitude"])

            except Exception as e:
                print(e)

            lst.add_xpath('href', ".//a[@class= 'card card--clickable']/@href")
            lst.add_xpath('price', ".//span[@class='card__price-value']/text()")
            lst.add_xpath('location', './/p[@class = "card__location"]/text()')
            lst.add_xpath('title', './/h2[@class="card__title card__title-link"]/text()')
            lst.add_xpath('type', './/p[@class="card__property-amenity card__property-amenity--property-type"]/text()')
            lst.add_xpath('bedrooms', './/p[@class="card__property-amenity card__property-amenity--bedrooms"]/text()')
            lst.add_xpath('bathrooms', './/p[@class="card__property-amenity card__property-amenity--bathrooms"]/text()')
            lst.add_xpath('floor_area', './/p[@class="card__property-amenity card__property-amenity--area"]/text()')
            lst.add_value('listing_url', url)

            yield lst.load_item()

        # Scraping next page also...
        next_page = response.xpath('//a[@class="pagination__link pagination__link--next"]/@href').get()
        if next_page is not None:
            yield response.follow(url = next_page, callback = self.parse)


# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(PropertyFinder)
    process.start()


