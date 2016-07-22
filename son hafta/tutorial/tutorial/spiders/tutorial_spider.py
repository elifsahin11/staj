#! /usr/bin/env python
#-*- coding: utf-8 -*-

import scrapy
from tutorial.items import TutorialItem
import json

class TutorialSpider(scrapy.Spider):
	name = "sahibinden"
	allowed_domains = ["sahibinden.com"]
	start_urls = ["https://www.sahibinden.com/son-1-ay"]

	def parse(self, response):
		for i in range(0, 980, 20): 		# 980 offset
			yield scrapy.Request("https://www.sahibinden.com/son-1-ay?pagingOffset=" + str(i), callback = self.parse_pages)


	def parse_pages(self, response):
		for href in response.xpath('//td[contains(@class, "searchResultsGalleryContent")]//div/a[contains(@class, "classifiedTitle")]//@href'):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback = self.parse_items)

	def parse_items(self, response):
		item = TutorialItem()
		item['information'] = {}
		item['features'] = {}

		for sel in response.xpath('//ul[contains(@class, "classifiedInfoList")]//li'):
			key = sel.xpath('./strong/text()').extract()[0].strip().encode('utf-8')
			value = sel.xpath('./span/text()').extract()[0].strip().encode('utf-8')
			
			item['information'][key] = value
		
		for sel in response.xpath('//div[contains(@class, "uiBoxContainer classifiedDescription")]//ul//li[contains(@class, "selected")]'):
			item['features'][sel.xpath('text()').extract()[0].strip().encode('utf-8')] = "True"
		
		for sel in response.xpath('//div[contains(@class, "uiBoxContainer classifiedDescription")]//ul//li[not(contains(@class, "selected"))]'):
			item['features'][sel.xpath('text()').extract()[0].strip().encode('utf-8')] = "False"

		for sel in response.xpath('//div[contains(@class, "classifiedDetailTitle")]'):
			item['title'] = sel.xpath('./h1/text()').extract()[0].encode('utf-8').strip()
		
		for sel in response.xpath('//div[contains(@class, "classifiedInfo")]'):
			price = sel.xpath('./h3/text()').extract()[0].encode('utf-8').strip().replace(" ", "")

			if "TL" in price:
				price = price.replace("TL", "")
			
			item['price_TL'] = price
			
		yield item