# Scraping Made in China

Python script for scrape sales name and contact numbers by using company url as the input. For getting to see the contact number appear on the front-end, a user at least login into madeinchina.com first.  

In this project, instead of do automation login, I prefer to [copy and paste](#copy-and-paste-the-cookies) the cookies using chrome extension named [EditThisCookies](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg).

I also use asynchronous programming for render and scrape multiple urls instead of using synchronous programming. It will save more time for scraping the bigger size of data.  

Last but not least, I also write a script for converting the output data ada csv file using `pandas` library.

___  
## Copy and Paste Cookies
<img src="./images/Screenshot_3.png" width=500 height=500 align="middle">
