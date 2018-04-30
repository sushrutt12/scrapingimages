from imagecrawler.items import MyImage
import datetime
import scrapy


class Crawler(scrapy.Spider):
	name = "image_spider"
	pages=0 # Static variable counting number of pages
	# URL of the page you want to obtain images from
	start_urls=["https://www.gettyimages.com/photos/chris-hemsworth?family=editorial&imagesize=xxxlarge&phrase=chris%20hemsworth&sort=best#license"]
	
	def parse(self, response):
		Crawler.pages+=1
		url = response.xpath('//*[@id="assets"]/article')
		data= url.xpath('//*[@id="assets"]/article').extract()
		for href in data: # Looping through each image from a list of images
			imglink = href[href.find('src'):]
			imglink = imglink[5:imglink.find('>')-1] # Url for the image
			title=href[href.find('target'):]
			title=title[8:title.find('>')-1]
			now = datetime.datetime.now() # The current date and time
			yield MyImage(title=title, createDate=now, image_urls=[imglink])
		
		if Crawler.pages  != 2: # Counting two pages for now
			next = response.xpath('//*[@id="next-gallery-page"]') # Get URL for next page
			if next is not None: # Check if there is a next page
				yield scrapy.Request("https://www.gettyimages.com"+next.xpath("@href").extract_first(), self.parse)