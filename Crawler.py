from Scraper import Scraper
from Json import CustomJSONFormatter
from CSV import CSV
import POS
import unicodedata
from datetime import date, datetime, timedelta
import _thread

class Crawler:
	def __init__(self, depth, sampleSize, keyword):
		self.depth = depth
		self.contents = []
		self.crawlContents = []
		self.titles = []
		self.linksCrawled = []
		self.datecreated = {}
		self.keyword = keyword
		self.sampleSize = sampleSize
		self.voidedTitles = ["BBC Homepage", "Sign in"]
		self.results = {}

		self.knownlinks = [".mp4"]
		today = str(date.today())
		self.csvFile = CSV(keyword + "," + today + ".csv", ["Word", "Tag", "Weight", "Link", "DateCreated"])

	def start(self):
		urlsToCrawl = []
		json = CustomJSONFormatter(self.keyword)
		articles = json.getValues("articles")

		for item in articles:
			urlsToCrawl.append(item["url"])
			self.contents.append(item["description"])
			self.titles.append(item["title"])
			self.datecreated[item["url"]] = item["publishedAt"]

		# for item in urlsToCrawl:
		# 	# print(item)
		# 	self.crawl(item, 0 , self.keyword, self.datecreated[item])
		print("")
		print("Links crawled:")

		posDict = {}

		# [(), ""] : weight
		for i in range(len(self.titles)):
			item = self.titles[i]
			url = urlsToCrawl[i]

			if "\\" not in item:
				tempDictForTitle = POS.POS(item)
				keys = tempDictForTitle.keys()

				for i in keys:
					urlList = (i, url)
					posDict[urlList] = tempDictForTitle[i]


		for i in range(len(self.contents)):
			title = self.titles[i]
			datecreated = self.datecreated[url]
			item2 = self.contents[i]
			url = urlsToCrawl[i]

			listOfKeysToUpdateUrl = []

			if item2 is not None:
				for node in item2:
					if not isinstance(node, str):
						sentence = node.find_all(text=True)
						for minisentence in sentence:
							tempDictForContents = POS.POS(minisentence, True)
							keys = tempDictForContents.keys()
							for i in keys:
								listUrl = (i, url)
								if listUrl not in posDict:
									posDict[listUrl] = tempDictForContents[i]
								else:
									posDict[listUrl] = posDict[listUrl] + tempDictForContents[i]
								listOfKeysToUpdateUrl.append(listUrl)
							break

					elif isinstance(node, str):
						tempDictForContents = POS.POS(item2)
						keys = tempDictForContents.keys()

						for i in keys:
							listUrl = (i, url)
							if listUrl not in posDict:
								posDict[listUrl] = tempDictForContents[i]
							else:
								posDict[listUrl] = posDict[listUrl] + tempDictForContents[i]
							listOfKeysToUpdateUrl.append(listUrl)
						break
	
		self.crawlContents = self.contents
		keys = posDict.keys()
		for i in keys:
			self.crawl(i[1], 0, self.keyword, posDict)
		
		for i in keys:
			print(i)
			print(posDict[i])
			print(self.datecreated[i[1]])

			newDict = {}
			newDict["Word"] = self.lowerCase(i[0][0])
			newDict["Tag"] = i[0][1]
			newDict["Weight"] = posDict[i]
			newDict["Link"] = i[1]

			date = self.datecreated[i[1]]
			dates = date.split("T")
			dates2 = dates[0].split("-")

			newDict["DateCreated"] = dates2[2] + "/" + dates2[1] + "/" + dates2[0]

			self.csvFile.push(newDict)	
		self.csvFile.save()

	def getContents(self):
		return self.contents

	def lowerCase(self, sentence):
		return sentence.lower()

	def crawl(self, link, depth, keyword, posDict):
		print("Depth of " + str(depth) + " : "+ link)

		if link in self.linksCrawled:
			return

		for item in self.linksCrawled:
			if link[:100] == item[:100]:
				return

		if depth >= self.depth:
			return

		self.linksCrawled.append(link)
		scraper = Scraper(link, keyword)
		hyperLinkList = scraper.scrapeLinks(link)
		articleDictionary = scraper.scrape('p')

		print(articleDictionary)

		for item in articleDictionary:
			if item not in self.crawlContents:
				self.crawlContents.append(item)

				if isinstance(item, str):
					tempDictForContents = POS.POS(item)
					keys = tempDictForContents.keys()

					for i in keys:
						listUrl = (i, link)
						if listUrl not in posDict:
							posDict[listUrl] = tempDictForContents[i]
						else:
							posDict[listUrl] = posDict[listUrl] + tempDictForContents[i]
						print(item)

		if len(self.crawlContents) + len(self.contents) <= self.sampleSize and len(articleDictionary) != 0 and len(self.linksCrawled) <= self.sampleSize:
			self.linksCrawled.append(link)
			if hyperLinkList is not None:
				for link in hyperLinkList:
					if link not in self.linksCrawled:
						if "ad" not in link:
							_thread.start_new_thread(self.crawl,(link, depth + 1, self.keyword, posDict,))

							# self.crawl(link, depth + 1, self.keyword, posDict)
	
	def getAbsoluteLink(self, link):
		pathList = link.split("/")
		protocol = pathList[0]
		host = pathList[2]
		return protocol + "//" + host


if __name__ == '__main__':
	keyword = "world cup winner"
	string  = "https://newsapi.org/v2/everything?q=" + keyword + "&sortBy=publishedAt&language=en&apiKey=a45eaf5ba58b49b98ff5c5052340e8b9"
	crawler = Crawler(2 , 100, keyword)
	crawler.start()
