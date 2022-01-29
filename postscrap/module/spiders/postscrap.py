import scrapy

class PostSpider(scrapy.Spider):
    name = 'scrap'
    allowed_domain='https://news.detik.com/'
    start_url = [
        'https://news.detik.com/indeks/?date=%s'
    ]

    def parse(self, response):

        print("processing:"+response.url)
        # extract data using xpath
        date = response.xpath("//article//div[@class='media__date']/span/@title").extract()
        title = response.xpath("//article//h3[@class='media__title;']/a/text()").extract()

        row_data = zip(title, date)

        #making extracted data row wise
        for item in row_data:
            # create a dictionary
            scraped_info = {
                # key value
                'page':response.url,
                'title':item[0],
                'date':item[1]
            }

            #yield or give the scraped info to scrapy
            yield scraped_info
