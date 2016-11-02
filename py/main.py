#!/usr/bin python

import learning
import stock
import twitter

url = "notSureYet.com"

def getNextTimeDat(date):

        # Get the Twitter data
    tdat = twitter.gather(url, date)

        # Check for errors

        # Get the stock data
    sdat = stock.gather(url, date)

        # Check for errors
