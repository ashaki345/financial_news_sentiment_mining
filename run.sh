#!/bin/sh

#Parse stock list into different format (looking back, this is very unnecessary)
python parseStocksList.py

#Get links of relevant articles from google news, write out to txt files
python googleNewsMiner.py

#Read all text files and download articles via links
python downloadLinks.py

#Perform sentiment analysis on resulting articles with NLTK, write to file
python sentimentAnalyzer.py

#Get results from yfinance and plot with matplotlib
python sentimentVsReality.py
