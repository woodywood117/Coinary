package coinary;

import java.io.*;
import java.net.*;

public class Main {

  // URL of server where PHP files are stored
  private static String serverURL = "https://example.com/";
  // Access key for authenticating with PHP files
  private static String coinaryAccessKey = "defaultKeyChangeBeforeUse";

  // ID of last tweet received for each of the Twitter handles
  private static String[] lastIDArray = new String[37];
  // Last response from Yahoo Finance for each stock symbol
  private static String[] lastStockResponseArray = new String[37];

  // Stores list of Twitter handles that are being scrapped
  private static String[] handleArray = {"3m", "amazon", "apple", "att",
      "bankofamerica", "boeing", "chevron", "cisco", "citi", "comcast",
      "cocacola", "disney", "exxonmobil", "facebook", "ford", "generalelectric",
      "google", "ibm", "intel", "mastercard", "mcdonalds", "microsoft",
      "netflix", "nvidia", "oracle", "pepsico", "qualcomm", "sprint",
      "tmobile", "teslamotors", "unionpacific", "verizon", "visa",
      "walgreens", "walmart", "wellsfargo", "yahoo"
  };

  // Stores list of stock symbols that are being scrapped
  private static String[] tickerArray = {"MMM", "AMZN", "AAPL", "T", "BAC",
      "BA", "CVX", "CSCO", "C", "CMCSA", "KO", "DIS", "XOM", "FB", "F", "GE",
      "GOOGL", "IBM", "INTC", "MA", "MCD", "MSFT", "NFLX", "NVDA", "ORCL",
      "PEP", "QCOM", "S", "TMUS", "TSLA", "UNP", "VZ", "V", "WBA",
      "WMT", "WFC", "YHOO"
  };

  public static void main(String[] args) {

    // Sets last Twitter ID for all handles to 0
    for (int j = 0; j < lastIDArray.length; j++) {
      lastIDArray[j] = "0";
    }
    // Sets last response from Yahoo Finance for each stock symbol to empty
    for (int k = 0; k < lastStockResponseArray.length; k++) {
      lastStockResponseArray[k] = "";
    }

    // Runs main logic loop in its own thread
    Thread mainLogicThread = new Thread() {
      public void run() {
        try {
          while (true) {
            for (int i = 0; i < handleArray.length; i++) {
              // Add to CSV with tweets for handle
              runCoinaryPHP(i, 100, handleArray[i]);
              // Add to CSV with data for stock symbol
              runYahooFinance(i, tickerArray[i]);
              System.out.printf("Tweets for @%s retreived.\n", handleArray[i]);
              System.out.printf("Stock prices for %s retreived.\n",
                tickerArray[i]);
              // Wait 5 seconds before continuing to next company
              Thread.sleep(5000);
            }
          }
        } catch(Exception e) {
          e.printStackTrace();
          System.exit(1);
        }
      }
    };
    mainLogicThread.start();
  }

  // Runs PHP file to scrape data from Twitter and store in CSV on web server
  public static void runCoinaryPHP(int index, int count, String handle) {
    Thread coinaryPHPThread = new Thread() {
      public void run() {
        try {
          URL serverCoinaryURL = new URL(serverURL + "tweets.php");
          URLConnection serverCoinaryConnection = serverCoinaryURL
            .openConnection(); // Creates HTTPS connection to server
          // Tells connection we're going to POST to server
          serverCoinaryConnection.setDoOutput(true);
          // Gets stream to POST data
          PrintStream serverCoinaryPrintStream = new PrintStream(
            serverCoinaryConnection.getOutputStream());
          // POST the access key for using coinary.php on server
          serverCoinaryPrintStream.printf("coinaryaccesskey=%s",
            coinaryAccessKey);
          // POST maximum tweets to receive
          serverCoinaryPrintStream.printf("&count=%d", count);
          // POST ID of newest tweet received
          serverCoinaryPrintStream.printf("&lastID=%s", lastIDArray[index]);
          // POST handle of account (exclude @)
          serverCoinaryPrintStream.printf("&handle=%s", handle);
          serverCoinaryPrintStream.close();
          // Opens connection to receive response
          BufferedReader serverCoinaryReader = new BufferedReader(
            new InputStreamReader(serverCoinaryConnection
            .getInputStream()));
          // Reads last ID from server
          String returnedID = serverCoinaryReader.readLine();
          // An ID has been returned, so tweets have been posted
          if (!returnedID.equals("")) {
            lastIDArray[index] = returnedID; // Save received ID as last ID
          }
          serverCoinaryReader.close();
        } catch(Exception e) {
          e.printStackTrace();
        }
      }
    };
    coinaryPHPThread.start();
  }

  // Runs PHP file to store data from Yahoo Finance on web server
  public static void runCoinaryTickerPHP(int i, String ticker, String data) {
    try {
      URL serverCoinaryStocksURL = new URL(serverURL + "stocks.php");
      URLConnection serverCoinaryStocksConnection = serverCoinaryStocksURL
        .openConnection(); // Creates HTTPS connection to server
      // Tells connection we're going to POST to server
      serverCoinaryStocksConnection.setDoOutput(true);
      // Gets stream to POST data
      PrintStream serverCoinaryStocksPrintStream = new PrintStream(
        serverCoinaryStocksConnection.getOutputStream());
      // POST the access key for using coinaryStocks.php on server
      serverCoinaryStocksPrintStream.printf("coinaryaccesskey=%s",
        coinaryAccessKey);
      // POST ticker
      serverCoinaryStocksPrintStream.printf("&ticker=%s", ticker);
      // POST data from Yahoo
      serverCoinaryStocksPrintStream.printf("&data=%s", data);
      serverCoinaryStocksPrintStream.close();
      BufferedReader serverCoinaryStocksReader = new BufferedReader(
        new InputStreamReader(serverCoinaryStocksConnection
        .getInputStream())); // Opens connection to receive response
      serverCoinaryStocksReader.close();
    } catch(Exception e) {
      e.printStackTrace();
    }
  }

  // Uses Yahoo Finance to request CSV with live stock data from ticker
  public static void runYahooFinance(int i, String ticker) {
    Thread yahooFinanceThread = new Thread() {
      public void run() {
        try {
          String stockFormat = "s=" + ticker + "\\&f=l1d1t1c1ohgv";
          URL yahooStocks = new URL("http://finance.yahoo.com/d/quotes.csv?" +
            stockFormat);
          // Creates connection to Yahoo Finance
          URLConnection yahooConnection = yahooStocks.openConnection();
          yahooConnection.setDoOutput(false); // No POST necessary
          BufferedReader yahooStocksReader = new BufferedReader(
            new InputStreamReader(yahooConnection.getInputStream()));
          // Read response, CSV as String
          String data = yahooStocksReader.readLine();
          yahooStocksReader.close();
          System.out.println(lastStockResponseArray[i].lastIndexOf(','));
          if (!lastStockResponseArray[i].equals("") && lastStockResponseArray[i]
            .lastIndexOf(',') != -1) {
            int lastIndexOfCommaInResponse = lastStockResponseArray[i]
              .lastIndexOf(',');
            if (!(data.substring(0, lastIndexOfCommaInResponse))
              .equals(lastStockResponseArray[i]
              .substring(0, lastIndexOfCommaInResponse)))
            { // If data minus trades has changed, add to CSV
              runCoinaryTickerPHP(i, ticker, data);
            }
          }
          else {
            // No last data to compare to, add to CSV
            runCoinaryTickerPHP(i, ticker, data);
          }
          lastStockResponseArray[i] = data;
        } catch(Exception e) {
          e.printStackTrace();
        }
      }
    };
    yahooFinanceThread.start();
  }
}
