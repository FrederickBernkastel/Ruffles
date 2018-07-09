from Scraper import Scraper

class Crawler:
	def __init__(self, link, depth):
		self.link = link
		self.depth = depth
		self.contents = []

	def start():
		self.crawl(self.link, self.depth)

	def getContents():
		return self.contents

	def crawl(self, link, depth):
		if depth < self.depth:
			scraper = Scraper(link)
			hyperlinkList = scraper.scrapeLinks()
			articleDictionary = scraper.scrapeBBCNewsArticle()

			self.append(articleDictionary)

			for link in hyperLinkList:
				self.crawl(link, 0)
