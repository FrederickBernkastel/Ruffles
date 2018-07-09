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
		try:
			return BeautifulSoup(urllib2.build_opener(urllib2.HTTPCookieProcessor).open(link),'html.parser')
		except ValueError as e:
			return None
		
	def scrape(self, tag):
		tagList = []
		if self.content is not None:
			for item in self.content.select(tag):
				tagList.append(item)
		return tagList

	# todo to filter out those without http infront of the link
	def scrapeLinks(self):
		sanitisedLinkList = []

		if self.content is not None:
			unsanitisedLinkList = self.content.find_all('a')
			for a in unsanitisedLinkList:
				item = a.get("href")
				if item is not None:
					if not "http" in item:
						item = "http://www.bbc.com" + item
					sanitisedLinkList.append(item)
			return sanitisedLinkList

		return None

	def scrapeBBCNewsArticle(self):
		listOfKnownHeaders = ["ideas-page__header", "story-body__h1"]
		filteredData = ["Email", "Facebook", "Messenger", "Twitter", "Pinterest", "Whatsapp", "LinkedIn"]

		h1List = []
		title = ""
		contents = []
		date = ""

		dict = {}

		h1List = self.scrape('h1')
		print h1List

		for item in h1List:
			title = item.encode_contents()
			if listOfKnownHeaders in item:
				print item.encode_contents()
				title = item.encode_contents()
				
		tempContent = self.scrape('p')
		if self.content is not None:
			for node in self.content.findAll('p'):
				contents.append(node.findAll(text=True))

			tempDivContents = self.content.findAll('div')
			for node in tempDivContents:
				if node.get("data-datetime") is not None:
					date = node.get("data-datetime")
					break

			dict["title"] = title
			dict["content"] = contents
			dict["date_created"] = date
			return dict

		return None

if __name__ == '__main__':
	scraper = Scraper("https://www.bbc.com/news/world-asia-44757804")
	dictionary = scraper.scrapeBBCNewsArticle()
	print dictionary
