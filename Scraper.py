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

	# todo to filter out those without http infront of the link
	def scrapeLinks(self):
		sanitisedLinkList = []
		unsanitisedLinkList = self.content.find_all('a')
		for a in unsanitisedLinkList:
			sanitisedLinkList.append(a.get("href"))

		return sanitisedLinkList

	def scrapeBBCNewsArticle(self):
		listOfKnownHeaders = ["ideas-page__header", "story-body__h1"]

		h1List = []
		title = ""
		contents = []
		date = ""

		h1List = self.scrape('h1')

		for item in h1List:
			if "story-body__h1" in item:
				title = item.encode_contents()

		contents = self.scrape('a')


	def defineTimeFromBBCNewsArticle(self, timeFormat):
		pass

