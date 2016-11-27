#!/usr/bin python

from argparse import ArgumentParser
import learning
import stock
import twitter
import datetime
from collections import OrderedDict

# Set all of the commandline flag options
parser = ArgumentParser()
parser.add_argument("-u", "--url", help="URL to pull data from", default="https://zebulonmorgan.com")
parser.add_argument("--handle", help="Twitter handle to use")
parser.add_argument("-s", "--symbol",required=True, help="Stock symbol to use")
parser.add_argument("-d", "--date", help="Start date", default="18.11.2016")
parser.add_argument("-e", "--end_date", help="End date", default="25.11.2016")
args = parser.parse_args()

tmp = args.end_date.split(".")
endDate = datetime.date(int(tmp[2]),int(tmp[1]),int(tmp[0]))
# Generate the primary data structures
tw = twitter.twitterStruct(args.handle, args.url, args.date)
st = stock.stockStruct(args.symbol, args.url, args.date)
ln = learning.tracker()

# Initialize first iteration of data
stock = st.nextVal()
if len(stock[2].split(":")[0]) < 2:
    stock[2] = "0" + stock[2] + " +0000"
stocDate = stock[1] + " " + stock[2]
stocDate = datetime.datetime.strptime(stocDate, "%m/%d/%Y %I:%M%p %z")
tweet = tw.nextTweet()
tweeDate = datetime.datetime.strptime(tweet[2], "%a %b %d %X %z %Y")
timeDict = {}
lastChange = 0
wordCount = 0

while st.Date < endDate:
    # print("Current Change is " + stock[3] + " at time " + str(stocDate) + "----------------------------------------------")
    while stocDate > tweeDate:
        if len(tweet) == 4:
            words = tweet[3].split(" ")
            for word in words:
                if word and ('@' not in word) and ("http" not in word):
                    if word not in timeDict.keys():
                        timeDict[word] = 0
                    timeDict[word] = timeDict[word] + 1
                    wordCount = wordCount + 1
        tweet = tw.nextTweet()
            # Tweet date format: Fri Nov 18 04:52:32 +0000 2016
        if len(tweet) == 4:
            tweeDate = datetime.datetime.strptime(tweet[2], "%a %b %d %X %z %Y")

    changeDiff = float(stock[3]) - lastChange
    for word in timeDict.keys():
        ln.addPair(word, ((changeDiff / wordCount) * timeDict[word]))

        # Save the last stock price change before proceeding
    lastChange = float(stock[3])
        # Get next stock value if it's available
    stock = st.nextVal()
    if len(stock[2].split(":")[0]) < 2:
        stock[2] = "0" + stock[2]
        # Stock date format: 11/17/2016 4:00pm
    stocDate = stock[1] + " " + stock[2] + " +0000"
    stocDate = datetime.datetime.strptime(stocDate, "%m/%d/%Y %I:%M%p %z")
    timeDict = {}
    wordCount = 0

endList = []
for word in ln.store.keys():
    endList.append((word, (sum(ln.store[word]) / float(len(ln.store[word])))))
    # print(word + ": ", (sum(ln.store[word]) / float(len(ln.store[word])))) 

endList = sorted(endList, key=lambda word: word[1])
print("The lowest 10 values are: ", endList[0:10])
print("The top 10 values are: ", endList[len(endList)-11:len(endList)-1])
