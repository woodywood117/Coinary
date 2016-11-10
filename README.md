# Coinary
Predicts stock prices and coorelates keywords from tweets to stock price variation

---

## Program Structure
The program is broken into two functional sections: the fetching of data, and the processing of data.
It uses three languages, Python, PHP, and Java. The Python portion of the
program handles the data processing. The PHP portion of the program handles all of
the authentication for twitter and fetching data. The Java portion of the program
is used handle the scheduling of data fetching.

### Fetching
--Put info on fetching data here--

### Processing
Processing the data primarily involves figuring out how to dynamically alter the different weighting
of words depending on how they are perceived to change the stock's trend. This involves keeping a
global table of words and all of the values associated with them up to that point in time.
