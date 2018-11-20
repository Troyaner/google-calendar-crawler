import exporter
from crawler import Crawler

calId = "bla"

gCrawler = Crawler()
myEvents = gCrawler.getYear(calId)
exporter.export(myEvents)