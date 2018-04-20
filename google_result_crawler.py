#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import urllib
import sys
import re
from selenium import webdriver
import urllib.parse
#import peewee
#from peewee import *
#from playhouse.db_url import connect
from selenium.webdriver.chrome.options import Options
import os
import string as str
#import MySQLdb
#import mysql.connector
import pymysql
import socket
import traceback
import datetime
import datetime
from datetime import timedelta
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
cnx = pymysql.connect(user='jared', password='iscae100',host='140.96.83.145',port=3306,database='gsearch', charset='utf8') 

def save_data(data):
    global cnx
    cursor = cnx.cursor()
    #sql = "insert into Serena.google_result_temp(begindate,enddate,keyword,numresult) values(%(begindate)s,%(enddate)s,%(keyword)s,%(numresult)s)  ON DUPLICATE KEY UPDATE numresult=%(numresult)s  "
    sql = "insert into Serena.google_result_temp6week(begindate,enddate,keyword,numresult) values(%(begindate)s,%(enddate)s,%(keyword)s,%(numresult)s)  "

    try:
        print(data) 
        cursor.execute(sql,data)
        cnx.commit()
        
    except: 
        print('exception savedata')
        error_string=traceback.format_exc()
        #print(type(error_string))
        if "Duplicate entry" in error_string :  
            print('dupliacate pass')
            pass
        else:
            print(error_string)

def get_progress(query): #目前爬到哪一個日期
    global cnx
    cursor = cnx.cursor()
    sql = "select min(begindate) from Serena.google_result_temp6week where keyword=\""+query+"\"  "
    #resultdt=datetime.datetime.now().date()
    resultdt=datetime.datetime.strptime("2017-11-25","%Y-%m-%d").date()
    try:
#        print(sql)
        cursor.execute(sql)
        for u in cursor:
            resultdt=u[0]
    except: 
        print('exception get_progress')
        traceback.print_exc()
    return resultdt


#options = webdriver.ChromeOptions()
#options.add_argument("--headless")
#options.binary_location='/usr/bin/google-chrome'
#driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=options)  # Optional argument, if not specified will search path.

#options.binary_location='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
driver = webdriver.Chrome('C:\\Users\\ua50049\\Desktop\\chromedriver_win32\\chromedriver.exe')  # Optional argument, if not specified will search path.





def process_page(driver):
    html = driver.page_source
    soup = BeautifulSoup(html,"lxml")
    
    elmt=soup.find('div',{'id':'resultStats'})
    print(elmt.text)
    sresult=re.search(u'約有 (.+) 項結果',elmt.text)
    if sresult is None:
        sresult=re.search(u'(.+) 項結果',elmt.text)
    print(sresult)
    print(sresult.group(1))
    return sresult.group(1).replace(",","")


'''
def get_prevweek(dt):
    ed=dt.strftime("%m/%d/%Y").replace("/","%2F")
    dt=dt+timedelta(days=-6)
    bg=dt.strftime("%m/%d/%Y").replace("/","%2F")
    return (bg,ed)
'''
def get_prevweek(dt):
    ed=dt.strftime("%m/%d/%Y").replace("/","%2F")
    if dt == datetime.datetime.strptime("2016-11-12","%Y-%m-%d").date():
        dt=dt+timedelta(days=-34)
    else :
        dt=dt+timedelta(days=-41)
    bg=dt.strftime("%m/%d/%Y").replace("/","%2F")
    return (bg,ed)


def mysearch(dt,query):
    global enddate
    global driver
#    n= datetime.datetime.now()
    bg,ed=get_prevweek(dt)
    fullurl='https://www.google.com.tw/search?rlz=1C1CHZL_enTW725TW725&biw=1243&bih=666&tbs=cdr%3A1%2Ccd_min%3A'+bg+'%2Ccd_max%3A'+ed+'&ei=DLJKWqXSLoaA8QXv9LagCg&q='+query+'&oq='+query
    print(fullurl)
    driver.get(fullurl)
    try:
        #搜尋結果為0的時候ww這一行會timeout error,所以做except例外處理,給值:0
        ww = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='resultStats'][string-length(text()) > 1]")))
        numresult=process_page(driver)
    except:
        numresult=0
    if dt == datetime.datetime.strptime("2016-11-12","%Y-%m-%d").date() :
        save_data({'begindate':dt+timedelta(days=-34),'enddate':dt,'keyword':query,'numresult':int(numresult)})
    else :
        save_data({'begindate':dt+timedelta(days=-41),'enddate':dt,'keyword':query,'numresult':int(numresult)})
    time.sleep(2)
    


enddate=datetime.datetime.strptime("2015-01-18","%Y-%m-%d")
n=datetime.datetime.strptime("2017-11-25","%Y-%m-%d")
#n=datetime.datetime.strptime("2016-09-15","%Y-%m-%d")



cursor = cnx.cursor()

print('select start:')   
   
sql="SELECT o.name, o.asCat FROM gsearch.search_list s, oneil.urcosme_prod_brand_google_segment o where s.id % 6 = 0 and o.brandid=s.pixid order by rand()"
cursor.execute(sql)
result=['深層卸妝油+DHC','mono eyes 眼影+Aritaum','單色眼影+ETUDE HOUSE','礦物控油蜜粉+innisfree','冰河醣蛋白保濕霜+契爾氏+or+KIEHLS','情挑誘光水唇膏+聖羅蘭+or+YSL'
,'蜂巢氣墊+珂莉奧+or+CLIO']


for u in cursor:   # 把要跑的keyword存到result list
    q=u[0]+'+'+ u[1]
    #result.append(q.replace("'",""))
    if ("KEVIN.MURPHY" not in q) and ("歐恩伊" not in q) and ("精油身體乳+專科" not in q) and("Sugar Scrub&Lip Balm" not in q): #精油身體乳+專科
        result.append(q)

print('result length:',len(result))
for query in result:  
    print(query)   
    n=get_progress(query)
    #n=None
    if n is None:
        n=datetime.datetime.strptime("2017-11-25","%Y-%m-%d").date()
        
    print('process get:',n)
    
    while n >= enddate.date():
        mysearch(n,query)
        if n == datetime.datetime.strptime("2016-11-12","%Y-%m-%d").date() :
            n=n+timedelta(days=-35)
        else :
            n=n+timedelta(days=-42)
   

print('close drive')
driver.close()
exit(1)
