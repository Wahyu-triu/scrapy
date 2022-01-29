# -*- coding: utf-8 -*-
import scrapy
import logging

from sqlalchemy import true

class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["worldometers.info/world-population/population-by-country"]
    start_urls = [
        'http://www.worldometers.info/world-population/population-by-country/'
    ]

    def parse(self, response):
       # countries = response.xpath("//td/a").getall() , for get all text
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name':name}, dont_filter=true)
                  
    def parse_country(self, response):
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").extract()
            population = row.xpath(".//td[2]/strong/text()").extract()
            perc_yearly_change = row.xpath(".//td[3]/text()").extract()
            yearly_change = row.xpath(".//td[4]/text()").extract()
            mediam_age = row.xpath(".//td[6]/text()").extract()
            density = row.xpath(".//td[8]/text()").extract()
            perc_urban_pop = row.xpath(".//td[9]/text()").extract()
            urban_pop = row.xpath(".//td[10]/text()").extract()
            yield {
               'country_name':name,
               'year':year,
               'population':population,
               'yearly change (%)':perc_yearly_change,
               'yeraly change':yearly_change,
               'median age':mediam_age,
               'density':density,
               'urban pop (%)':perc_urban_pop,
               'urban pop':urban_pop
               }
    
    # good code but try to scrap more data
    # like population increasment (in perc), or else. thank you, you're doing great job.