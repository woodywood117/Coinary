#!/usr/bin python

import csv
import httplib

def gather(url, date):

        # Generate the connection to server
    conn = httplib.HTTPConnection(url)

        # Make request for specified date
    conn.request("GET", "/stock_"+date)

        # Read the response from the socket
    resp = conn.getresponse()

        # Check that we got a response
    if resp.status != 200:
            # If we didn't, return error code
        return resp.status

        # Process the request
    output = resp.read()

        # Close the connection
    conn.close()

        # Return the output
    return output


def nextVal():


