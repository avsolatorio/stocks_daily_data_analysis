#-------------------------------------------------------------------------------
# Name:        stocksDailyTransactionsDownloader.py
# Purpose:
#
# Author:      avsolatorio
#
# Created:     10/06/2014
# Copyright:   (c) avsolatorio 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from web_login import getLoginAccess
import bz2
import cPickle
import datetime
import re
import os
import time


def trimNuisancePartFromResponse(response):
    pattern = '<form action=[\w\W]*?</form>'    #Find a way to complete regex: <form action="transactions.cshtml" method="get">
    return re.findall(pattern, response)[0]

def getCurrentDateInString():
    date = datetime.datetime.now()
    return date.strftime('%m_%d_%Y')    #Equivalent to: 06_10_2014 which is June 10, 2014

def compressAndSaveData(data, file_name):
    bz2_file = bz2.BZ2File(file_name, 'w')
    bz2_file.write(data)
    bz2_file.close()


def main():
    symbols_names = cPickle.load(open('PSE_LISTED_STOCKS_SYMBOLS_NAMES.dict'))
    url = raw_input("Please input the url for the site that you want to access: ")
    access_site = url + '/Public/Default.aspx'
    current_date = getCurrentDateInString()
    htmlOpener = getLoginAccess(access_site)

    symbols = sorted(symbols_names.keys())

    for symbol in symbols:
        print "Processing data for: %s" % symbol.upper()
        response = htmlOpener.open('%s/Infinity/Transactions.cshtml?Symbol=%s' % (url, symbol.upper()))
        data = response.read()

        final_data = trimNuisancePartFromResponse(data)

        file_name = './%s/%s_%s.htm.bz2' % (symbol.upper(), symbol.upper(), current_date)
        if not os.path.isdir(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))

        compressAndSaveData(final_data, file_name)

        time.sleep(0.2)

if __name__ == '__main__':
    main()
