from Scraper import Scraper

class Crawler:
	def __init__(self, link, depth, keyword):
		self.link = link
		self.depth = depth
		self.contents = []
		self.linksCrawled = []

	def start(self):
		self.crawl(self.link, 0, keyword)

	def getContents(self):
		return self.contents

	def crawl(self, link, depth, keyword):
		if depth < self.depth:
			scraper = Scraper(link, keyword)
			hyperLinkList = scraper.scrapeLinks()
			articleDictionary = scraper.scrapeBBCNewsArticle()

			self.contents.append(articleDictionary)
			self.linksCrawled.append(link)
			if hyperLinkList is not None:
				for link in hyperLinkList:
					print "Depth of " + str(depth) + " @ link: " + link  
					if link not in self.linksCrawled:
						self.crawl(link, 0 + 1)
			

crawler = Crawler("http://www.bbc.com", 2)
crawler.start()
