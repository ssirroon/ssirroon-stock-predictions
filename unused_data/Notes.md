
**Delete this file before submitting the project**


Things to write unit tests for:

- In pull_stock_info.py, make sure timedelta does addition correctly
- In pull_stock_info.py, check that the string is being properly converted to datetime
- In all .py files, check that every function has a docstring


How to narrow down r/wallstreetbets posts:
- filter out promoted posts
- filter out posts containing videos
- keep posts containing a dollar sign followed by one or more capital letters (usually telling users to invest)
- keep posts containing a dollar sign followed by a number (usually indicates a merger)
    - look for company name in the post
- keep posts with a 1-4 character string of uppercase letters (probably a ticker symbol)?
    - search to see if it is a ticker symbol?
- key words to include: watch, up, deal, buys
- key words to remove/uncapitalize: government acronyms (US, USPS, EPA, etc.), APES? (appears to be a nickname for investors short selling stocks), SALE, STOCK, CEO, AI, FREE

Questions for Steve:
What types of functions can we write unit tests for?
- Functions that do things, rather than pull web info or graph
How do we do documentation (docstrings, etc) on the unit tests?
- Make a docstring for each function and a comment for each case
Do we want to keep intermediate files/functions to show progress?
- Make a new folder and don't use it in the computational essay