# Scrape madeinchina.com

Python script for scrape sales name and contact numbers using company url as the input. To see the contact number appear on the front-end, a user at least logged in to madeinchina.com.  

In this project, instead of do automation login, I prefer to just do [copy and paste](#copy-and-paste-cookies) the cookies using chrome extension named [EditThisCookies](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg).

I also use asynchronous programming for render and scrape multiple urls at single run (it works well in my computer max. 80 urls, in this code I only put 40 urls). The reason is, it will save more time for scraping the bigger size of data.  

Last but not least, I also write a script for converting the output data to csv file using `pandas` library and `to_csv()` method.  

To see how it's work both on scraping single url or multiple url, go to "/test/" folder.

___  
## Copy and Paste Cookies
<img src="./images/screenshots.png" width=500 height=500 align="middle">

After you are logged in, click the export, go to /data/cookies.json open it using text editor, and then paste it there.
