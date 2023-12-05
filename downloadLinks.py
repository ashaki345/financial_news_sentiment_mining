import os
import glob
import pandas as pd
from newspaper import Article
from newspaper import Config

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

files = glob.glob("./linkFiles/*.txt")
for f in files:
    count = 1
    print(f)
    fname = f.split("./linkFiles/")[1]
    print(fname)
    fname = f.split(".txt")[0]
    savename = fname.split(".txt")[0]
    savename = fname.split("linkFiles/")[1]
    dirname = "./stockArticles/" + savename.strip()
    print(dirname)
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    else:
        print("Exists: " + dirname)
        continue
    with open(f,"r") as file:
        for line in file:
            link = line.split("|")[1].strip()
            date = line.split("|")[0].strip()
            article = Article(link,config=config)
            try:
                article.download()
                article.parse()
                article.nlp()
            except:
                count+=1
                continue
            dict = {}
            dict['Date'] = date
            dict['Title']=article.title
            dict['Article']=article.text
            dict['Summary']=article.summary
            out = pd.DataFrame([dict])
            out.to_csv(dirname+"/"+str(count)+".csv")
            count += 1
    file.close()
