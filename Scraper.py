from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import urllib
from urllib.request import urlopen
import http.client
import string
from ast import literal_eval

# pip install BeautifulSoup4

class Scraper:
	def __init__(self, link, keyword):
		self.link = link
		self.content = self.store(link)
		self.keyword = keyword

	def store(self, link):
		try:
			# bs = BeautifulSoup(urllib.build_opener(urllib.HTTPCookieProcessor).open(link),'html.parser')
			bs = BeautifulSoup(urlopen(link) , "html.parser")
			return bs
		except urllib.error.HTTPError:
			return None
		except urllib.error.URLError:
			return None
		except ValueError:
			return None
		except:
			return None


	def scrape(self, tag):
		tagList = []
		if self.content is not None:
			for node in self.content.findAll(tag):
				paragraph = node.findAll(text=True)
				for sentence in paragraph:
					keywordList = self.keyword.split(" ")
					for keyword in keywordList:
						if keyword in sentence.lower() and len(sentence) > 100:
							tagList.append(node.findAll(text=True))
							break
		return tagList

	# todo to filter out those without http infront of the link
	def scrapeLinks(self, absoluteLink):
		sanitisedLinkList = []

		if self.content is not None:
			unsanitisedLinkList = self.content.find_all('a')
			for a in unsanitisedLinkList:
				item = a.get("href")
				if item is not None:
					if not "http" in item:
						item = absoluteLink + item
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

		for item in h1List:
			title = item.encode_contents()
			if listOfKnownHeaders in item:
				# print(item.encode_contents())
				title = item.encode_contents()
				
		tempContent = self.scrape('p')
		if self.content is not None:
			for node in self.content.findAll('p'):
				paragraph = node.findAll(text=True)
				for sentence in paragraph:
					if self.checkIfContainsKeywordPerParagraph(sentence):
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


	def checkIfContainsKeywordPerParagraph(self, sentence):
		if self.keyword in sentence:
			return True
		return False

if __name__ == '__main__':
	scraper = Scraper("http://www.businessinsider.com/13-burning-personal-finance-questions-2013-3/?IR=T", "")
	dictionary = scraper.scrape('p')

	list = []
	# print(dictionary)
	for item in dictionary:
		for item2 in item:
			item2 = item2.replace("  ", "").replace("\n", " ").replace("\r", " ")
			list.append(item2)

	for item in list:
		print(item)
			
	
