import json
import arrow
from datetime import date, datetime, timedelta
from Scraper import Scraper

class CustomJSONFormatter:
	def __init__(self, keyword):
		intiialKeyword = keyword
		keyword = keyword.replace("[,;!.`~'\"]", "")
		keyword = keyword.replace(" ", "%20")

		today = str(date.today())
		print(today)
		fromdate = str(datetime.now() - timedelta(days=30))
		fromdate = fromdate.split(" ")[0]
		print(fromdate)

		# link  = "https://newsapi.org/v2/everything?q=" + keyword + "sources=bbc-news&sortBy=publishedAt&language=en&apiKey=a45eaf5ba58b49b98ff5c5052340e8b9"
		link  = "https://newsapi.org/v2/everything?q=" + keyword + "&from=" + fromdate + "&to=" + today + "&sortBy=popularity&language=en&apiKey=a45eaf5ba58b49b98ff5c5052340e8b9"

		scraper = Scraper(link , intiialKeyword)
		self.jsondata = scraper.content
		self.jsonObj = json.loads(str(self.jsondata))

	def getValues(self, item):
		return self.jsonObj[item]

if __name__ == '__main__':
	keyword = "Sample data"
	jsonParser = CustomJSONFormatter(keyword)
