import glob
import os
import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as pt

start = datetime.datetime(2018,1,1)
end = datetime.datetime(2018,12,31)
print(start)
print(end)

with open("./stockList.txt","r") as stockList:
    for s in stockList:
        stockAbbrev = s.split("|")[0].strip()
        stockName = s.split("|")[1].strip().replace(" ","_")
        files = glob.glob("./stockArticles/"+stockName+"/*sentiment.txt")
        articles = []
        for f in files:
            with open(f,'r') as article:
                for line in article:
                    date = line.split("|")[0].strip()
                    sent = line.split("|")[1].strip()
                    try: 
                        month = date[0:3:1]
                        day = date[4:5:1].strip()
                        year = date[7:].strip()
                        month = datetime.datetime.strptime(month,"%b")
                        month = month.month
                        jdstr = str(year)+"."+str(month)+"."+str(day)
                        dt = datetime.datetime.strptime(jdstr,"%Y.%m.%d")
                        tt = dt.timetuple()
                        jd = tt.tm_yday
                        articles.append({"Day" : jd, "Sentiment": sent})
                    except ValueError:
                        continue
        articles = sorted(articles,key = lambda k: k['Day'])
        if not os.path.isfile("./stockArticles/"+stockName+"/results.txt"):
            continue
        stock = yf.download(stockAbbrev,start=start,end=end)
        print(len(stock['Close']))

        stock_init = stock
        stock = stock.stack().reset_index().rename(index=str, columns={"level_1": "Symbol"}).sort_values(['Symbol','Date'])

        print(stock['Date'])
        yfjd = []
        for d in range(len(stock['Date'])):
            date = stock['Date'][d]
            try: 
                date = date.date()
                date = date.timetuple()
                jd = date.tm_yday
                yfjd.append(jd)
            except ValueError:
                continue

        pt.plot(range(len(stock_init['Close'])),stock_init['Close'],'k-')
        for art in range(len(stock_init['Close'])):
            try:
                sent = articles[art]
            except IndexError:
                break
            stday = sent['Day']
            sent = sent['Sentiment']
            try:
                plotIdx = yfjd.index(stday)
            except ValueError:
                plotIdx = yfjd.index(min(yfjd,key=lambda x:abs(x-stday)))
            if sent == '+':
                pt.plot(plotIdx,stock_init['Close'][plotIdx],'g.',linewidth=15)
            elif sent == '-':
                pt.plot(plotIdx,stock_init['Close'][plotIdx],'r.',linewidth=15)
            elif sent == '.':
                pt.plot(plotIdx,stock_init['Close'][plotIdx],'k.',linewidth=15)
        pt.xlabel('YTD')
        pt.ylabel('Closing Stock Price')
        ax = pt.axes()

        line = 1
        pos = 0
        neg = 0
        with open("./stockArticles/"+stockName+"/results.txt") as res:
            for num in res:
                if line == 1:
                    pos = float(num)
                    line += 1
                else:
                    neg = float(num)

        if pos > neg:
            pt.title (stockName + " 2018 stock price : Overall Positive Sentiment")
        else:
            pt.title (stockName + " 2018 stock price : Overall Negative Sentiment")

        pt.savefig("./resultPlots/"+stockName+".png")
        pt.cla()
        pt.clf()
        pt.close()

