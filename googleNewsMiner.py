from GoogleNews import GoogleNews
import time
from progress.bar import Bar
import os
import pandas as pd

toolbar_width = 40
numStocks = 505
pwd = os.getcwd()

#using the Google News API solved the issue of sorting by date 
#using these parameters!
gn = GoogleNews(start="01/01/2018",end="12/31/2018",lang="en",encode="utf-8")

bar = Bar("Collecting Articles", max=numStocks)
with open("./stockList.txt","r") as stockList:
    stockProgress = 1
    for stock in stockList:
        stockAbbrev = stock.split("|")[0].strip()
        stockName = stock.split("|")[1].strip()
        searchString = stockAbbrev + " stock"
        textname = stockName.replace(" ","_") + ".txt"
        if os.path.isfile(textname) and os.stat(textname).st_size > 0:
            print("Exists: " + textname)
            continue
        gn.search(searchString)
        with open(textname,"w") as outfile:
            for i in range(10):
                df = pd.DataFrame(gn.page_at(i))
                stockArticles = []
                textname = stockName.replace(" ","_") + ".txt"
                for idx in df.index:
                    print(df['link'][idx].strip()) 
                    outfile.write(df['date'][idx] + " | " + df['link'][idx].strip() + "\n")
        gn.clear()
        outfile.close()
        bar.next()
bar.finish()
