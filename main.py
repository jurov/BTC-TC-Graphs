import urllib2
import json
import math
import pylab
import matplotlib.finance

dsecurity = raw_input("Enter security (TAT.ASICMINER): ")
dperiod = raw_input("Enter period in seconds (36000 would be 10 mins): ")

data = urllib2.urlopen("https://btct.co/api/tradeHistory/" + dsecurity + "?range=all").read()

parse = json.loads(data)

print "orig elements: " + str(len(parse))

period = int(dperiod)
start = int(math.floor(float(min(parse, key = lambda item:int(item["timestamp"]))["timestamp"])/float(period))*period)/period
stop  = int(math.ceil (float(max(parse, key = lambda item:int(item["timestamp"]))["timestamp"])/float(period))*period)/period
size = stop - start + 1

plot = [[] for i in range(size)]

print start
print stop
print size

for i in range(len(parse)):
	j = parse[i]

	print j["timestamp"]

	index = int(math.floor(float(j["timestamp"])/float(period))*period)/period - start

	print index

	plot[index].append(j)

elements = 0

for a in plot:
	elements += len(a)

print "final elements: " + str(elements)

quotes = []

for period in range(len(plot)):
	try:
		qopen  = float(min(plot[period], key = lambda item:int(item["timestamp"]))["amount"])
		qclose = float(max(plot[period], key = lambda item:int(item["timestamp"]))["amount"])
		qhigh  = float(max(plot[period], key = lambda item:float(item["amount"]))["amount"])
		qlow   = float(min(plot[period], key = lambda item:float(item["amount"]))["amount"])
		qtime = period
		quote = (qtime, qopen, qclose, qhigh, qlow)
		quotes.append(quote)
	except ValueError:
		pass

ax = pylab.figure().add_subplot(111)

matplotlib.finance.candlestick(ax, quotes, width=0.6)
pylab.show()