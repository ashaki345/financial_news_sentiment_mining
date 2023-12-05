import csv

with open("./stockList.txt","w") as outfile:
    with open("./stocks.csv") as csvfile:
        stockReader = csv.reader(csvfile,delimiter=",")
        for row in stockReader:
            outfile.write(row[0] + " | " + row[1] + "\n")
    csvfile.close()
outfile.close()
