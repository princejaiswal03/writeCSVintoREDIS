from datetime import datetime,timedelta
import csv
import requests,io,zipfile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import redis

bhavCopyBseUrl = 'http://www.bseindia.com/markets/equity/EQReports/BhavCopyDebt.aspx?expandable=3'

#function to download zip Bhav Copy file
def downloadBhavCopyZip(bhavCopyBseUrl):
    downloadedFile = None
    
    #settting dateof today
    today = datetime.now()- timedelta(days=2)
    dd = today.strftime('%d')
    mm = today.strftime('%b')
    yyyy = today.strftime('%Y')
    
    driver = webdriver.Chrome('/home/raj/Downloads/chromedriver_linux64/chromedriver')
    driver.get('https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx')
    #select day
    driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_fdate1']/option[text()='%s']"%(dd)).click()
    
    #select month
    driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_fmonth1']/option[text()='%s']"%(mm)).click()
    
    #select year
    driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_fyear1']/option[text()='%s']"%(yyyy)).click()

    #Click submit button
    driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_btnSubmit"]').click()
    
    #Click on download link
    driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_btnSubmit"]').click()

    try:
        downloadLink = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_btnHylSearBhav"]')
        downloadLink = downloadLink.get_attribute('href')

        zipFile = requests.get(downloadLink)
        z = zipfile.ZipFile(io.BytesIO(zipFile.content))
        z.extractall('zips')
        downloadedFile = str('zips'+'/'+z.namelist()[0])

    except NoSuchElementException:
        print('No Download available for yesterday !')
    return downloadedFile

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


#function to connect redis
def connectRedis():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r


#function to save csv data into redis
def saveDataToRedis(data):
    r = connectRedis()
    r.flushall()
    for item in data:
        r.hmset(item['SC_CODE'],item)
    r.set('dataSaveOn',str(datetime.today().day))

#function to get record by SC_CODE
def getRecordByScCode(SC_CODE):
    recod = None
    r = connectRedis()
    if r.exists(SC_CODE):
        record = r.hgetall(SC_CODE)
    return record



#function to perform all task
def performAll():
    tmpFile = downloadBhavCopyZip(bhavCopyBseUrl)
    tmpData = readDataFromCsv(tmpFile)
    saveDataToRedis(tmpData)

    #finding first key
    r = connectRedis()
    keys = r.keys('*')[0]
    firstRecord = getRecordByScCode(keys)
    print(firstRecord)



performAll()

