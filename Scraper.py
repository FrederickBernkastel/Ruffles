from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib2

# pip install BeautifulSoup4

class Scraper:
	def __init__(self, link):
		self.link = link
		self.content = self.store(link)

	def store(self, link):
		return BeautifulSoup(urllib2.urlopen(link).read(), 'html.parser')

	def scrape(self, tag):
		tagList = []
		for item in self.content.select(tag):
			tagList.append(item)
			print item
		return tagList

	#todo to filter out those without http infront of the link
	def scrapeLinks(self):
		sanitisedLinkList = []
		unsanitisedLinkList = self.content.find_all('a')
		for a in unsanitisedLinkList:
			sanitisedLinkList.append(a.get("href"))		

		return sanitisedLinkList


# # testing of scraper
# scrape = Scraper("https://www.singaporetech.edu.sg/")
# print scrape.scrapeLinks()

