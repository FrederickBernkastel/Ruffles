from Crawler import Crawler
import Search
import POS

class Entry:
	def __init__(self, query):
		self.query = ""
		filterWords = POS.POS(query)

		for item in filterWords:
			if self.query == "":
				self.query += item[0]
			else:
				self.query += " " + item[0]

		print(self.query)
		self.crawler = Crawler(2, 1000, self.query)
		self.crawler.start()

	def start(self):
		csvFileName = self.query + ".csv"
		print(csvFileName)
		g = Search.load_csv(f=csvFileName)

		return str(g.search(self.query))

if __name__ == '__main__':
	entry = Entry("how to save your money?")
	print(entry.start())
