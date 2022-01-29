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
            yield {
               'country_name':name,
               'year':year,
               'population':population
               }