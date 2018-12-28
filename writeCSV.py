import csv
import requests,io,zipfile
from bs4 import BeautifulSoup

bhavCopyBseUrl = 'http://www.bseindia.com/markets/equity/EQReports/BhavCopyDebt.aspx?expandable=3'

#function to download zip Bhav Copy file
def downloadBhavCopyZip(bhavCopyBseUrl):
    downloadedFile = None
    urlContent = requests.get(bhavCopyBseUrl)
    print(urlContent.text)
    downloadedFile = urlContent

#function read the csv file
def readDataFromCsv(filename):
    returnCsvData = []
    #csvData = csv.reader(open(filename,'r'))
    #for row in csvData:
    #    print(row)
    #    print(type(row))  #  return list type
    #    break

    csvData = csv.DictReader(open(filename,'r'))
    for row in csvData:
        #print(row)
        #print(type(row))   # return collections.OrederedDict type
        #print(dict(row))
        returnCsvData.append(dict(row))
    return returnCsvData;



tmp = downloadBhavCopyZip(bhavCopyBseUrl)
print(tmp)
