# Stonks - A Reddit Story

### Contributors: Andrew DeCandia, Emma Fox, and Shamama Sirroon

This project creates a way to determine whether /r/wallstreetbets gives accurate predictions of what stocks will be good to invest in. We compare the ROI of recommended stocks to the S&P 500.

We make use of multiple APIs in order to obtain data from Reddit and Alpaca Markets.

## Set Up

To be able to run these files, we installed the following libraries and packages:
* `pip install alpaca_trade_api`
* `pip install datetime`
* `pip install matplotlib`
* `pip install numpy`
* `pip install pandas`
* `pip install pmaw`
* `pip install re`
* `pip install time`

We were required to create an account and credentials to access the Alpaca Markets API. Our credentials are in a file that is ignored by Git, but they are still necessary to pull data. The website for the Alpaca Market API is linked: https://alpaca.markets/docs/api-references/market-data-api/stock-pricing-data/. The GitHub also has more information on how to set up using the API: https://github.com/alpacahq/alpaca-trade-api-python. The PMAW API does not require credentials.

Regarding our data visualizations, we used matplotlib to generate a few different kinds of graphs. We created line graphs (using the LineCollection, ColorMap, and BoundaryNorm functions to determine whether a stock price was increasing or decreasing) and bar graphs to showcase the difference in Reddit and the S&P 500 stock prices.