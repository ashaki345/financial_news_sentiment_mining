import csv
import glob
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from progress.bar import Bar
import re

stocks = glob.glob("./stockArticles/*")

SIA = SentimentIntensityAnalyzer()
lanc = WordNetLemmatizer()

bar = Bar("Analyzing Stock:",max=508)
for s in stocks:
    files = glob.glob(s+"/*")
    posSum = 0
    negSum = 0
    neuSum = 0 
    for f in files:
        if not f.endswith(".csv"):
            continue
        with open(f,"r") as csvfile:
            print(f.split(".csv")[0])
            reader = csv.reader(csvfile,delimiter=',')
            count = 1
            for row in reader:
                if count==1:
                    count += 1
                    continue
                try:
                    date = row[1]
                    summary = row[2]
                    stemmed = []
                    #Remove stopwords and stem
                    for word in summary.split():
                        word = word_tokenize(word)[0]
                        if word in stemmed:
                            continue
                        if word in stopwords.words():
                            summary.replace(word,"")
                            continue
                        stemmed.append(word)
                        summary.replace(word,lanc.lemmatize(word))
                    stemmed = []
                    content = row[3]
                    for word in content.split():
                        word = word_tokenize(word)[0]
                        if word in stemmed:
                            continue
                        if word in stopwords.words():
                            content.replace(word,"")
                            continue
                        stemmed.append(word)
                        content.replace(word,lanc.lemmatize(word))
                except IndexError:
                    continue
                summaryScores = SIA.polarity_scores(summary)
                contentScores = SIA.polarity_scores(content)
                ps = (summaryScores['pos'] + contentScores['pos'])
                posSum += ps                
                ns = (summaryScores['neg'] + contentScores['neg'])
                negSum += ns
                with open(f.split(".csv")[0].strip() + "_sentiment.txt","w") as sentOut:
                    if ps > ns:
                        sentOut.write(date + " | +")
                    elif ns > ps:
                        sentOut.write(date + " | -")
                    elif ps == ns:
                        sentOut.write(date + " | .")
                sentOut.close()
        csvfile.close()
    bar.next()
    with open(s+"/results.txt","w") as outfile:
        outfile.write(str(posSum) + "\n")
        outfile.write(str(negSum) + "\n")
