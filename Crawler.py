from Scraper import Scraper
from Json import CustomJSONFormatter
import POS
import unicodedata

class Crawler:
	def __init__(self, link, depth, sampleSize, keyword):
		self.link = link
		self.depth = depth
		self.contents = []
		self.titles = []
		self.linksCrawled = []
		self.datecreated = {}
		self.keyword = keyword
		self.sampleSize = sampleSize

		self.voidedTitles = ["BBC Homepage", "Sign in"]

	def start(self):
		urlsToCrawl = []
		json = CustomJSONFormatter(keyword)
		articles = json.getValues("articles")

		for item in articles:
			urlsToCrawl.append(item["url"])
			self.contents.append(item["description"])
			self.titles.append(item["title"])
			self.datecreated[item["url"]] = item["publishedAt"]

		for item in urlsToCrawl:
			# print(item)
			self.crawl(item, 0 , self.keyword, self.datecreated[item])
		
		print("")
		print("Links crawled:")

		posList = []
		for item in self.titles:
			if "\\" not in item:
				tempDictForTitle = POS.POS(item)
				posList.append(tempDictForTitle)

		for item2 in self.contents:
			for node in item2:
				if not isinstance(node, unicode):
					sentence = node.find_all(text=True)
					for minisentence in sentence:
						tempDictForContents = POS.POS(minisentence, True)
						break
				elif isinstance(node, str):
					tempDictForContents = POS.POS(item2)
					posList.append(tempDictForContents)
					break


	def getContents(self):
		return self.contents

	def crawl(self, link, depth, keyword, date):
		print(link)
		if depth <= self.depth and link not in self.linksCrawled:
			parentLink = link
			scraper = Scraper(link, keyword)
			hyperLinkList = scraper.scrapeLinks(link)
			articleDictionary = scraper.scrape('p')

			for item in articleDictionary:
				if item not in self.contents:
					self.contents.append(item)
					print item

			if len(self.contents) <= self.sampleSize and len(articleDictionary) == 0 :
				self.linksCrawled.append(link)
				if hyperLinkList is not None:
					for link in hyperLinkList:
						if link not in self.linksCrawled:
							if "ad" not in link:
								self.crawl(link, 0 + 1, self.keyword, date)
	
	def getAbsoluteLink(self, link):
		pathList = link.split("/")
		protocol = pathList[0]
		host = pathList[2]
		return protocol + "//" + host


if __name__ == '__main__':
	keyword = "cryptocurrency"
	string  = "https://newsapi.org/v2/everything?q=" + keyword + "&sortBy=publishedAt&language=en&apiKey=a45eaf5ba58b49b98ff5c5052340e8b9"

	crawler = Crawler("http://www.businessinsider.com/13-burning-personal-finance-questions-2013-3/?IR=T", 1 , 20, keyword)
	crawler.start()
