import exporter
from crawler import Crawler

calId = "o1q2lvjkliar23irk4bv34pf60@group.calendar.google.com"

gCrawler = Crawler()
myEvents = gCrawler.getYear(calId)
exporter.export(myEvents)