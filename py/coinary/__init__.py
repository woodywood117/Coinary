#!/usr/bin python

from argparse import ArgumentParser
import learning
import stock
import twitter

# Set all of the commandline flag options
parser = ArgumentParser()
parser.add_argument("-u", "--url", help="URL to pull data from", default="https://zebulonmorgan.com")
parser.add_argument("--handle", help="Twitter handle to use")
parser.add_argument("-s", "--symbol",required=True, help="Stock symbol to use")
parser.add_argument("-d", "--date", required=True, help="Start date", default="10.11.2016")
args = parser.parse_args()

# Generate the primary data structures
tw = twitter.twitterStruct(args.handle, args.url, args.date)
st = stock.stockStruct(args.symbol, args.url, args.date)
# ln = learning.tracker()

tweet = tw.nextTweet()
print(tweet, tweet[3].split(" "))

stock = st.nextVal()
print(stock)
stock = st.nextVal()
print(stock)
stock = st.nextVal()
print(stock)
stock = st.nextVal()
print(stock)
stock = st.nextVal()
print(stock)
