#!/usr/bin python

from optparse import OptionParser
import learning
import stock
import twitter

# Set all of the commandline flag options
parser = OptionParser()
parser.add_option("-u", "--url", help="URL to pull data from", metavar="URL")
parser.add_option("-h", "--handle", help="Twitter handle to use", metavar="HAN")
parser.add_option("-s", "--symbol", help="Stock symbol to use", metavar="SYM")
parser.add_option("-d", "--date", help="Start date", metavar="DATE")
(options, args) = parser.parse_args()

# Assign variables / Check for bad input
url = options.URL
if not url:
    url = "https://zebulonmorgan.com"
if not date:
    date = "11.07.2016"
if (not options.SYM) or (not options.HAN):
    exit(1)


# Generate the primary data structures
tw = twitter.twitterStruct(url, "11.07.2016", tHandle)
st = stock.stockStruct(url, "11.07.2016", sSymbol)
# ln = learning.tracker()

print tw.nextTweet()
print st.nextVal()
