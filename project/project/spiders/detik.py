import scrapy

class PostSpider(scrapy.Spider):
    name = 'detik'
    allowed_domain='https://news.detik.com/'
    start_urls = [
        'https://news.detik.com/indeks/?date=%s'
    ]

    custom_setting={
        'FEED_URI':'detik_%(time)s.json',
        'FEED_FORMAT':'json'
    }
    def parse(self, response):

        print("processing:"+response.url)
        # extract data using xpath
        date = response.xpath('//article//div[@class="media__date"]/span/@title').extract()
        title = response.xpath('//article//h3[@class="media__title"]/a/text()').extract()

        row_data = zip(title, date)

        #making extracted data row wise
        for item in row_data:
            # create a dictionary
            scraped_info = {
                # key value
                'page':response.url,
                'title':item[1],
                'date':item[0]
            }

            #yield or give the scraped info to scrapy
            yield scraped_info
