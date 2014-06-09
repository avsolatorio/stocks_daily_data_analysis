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

def main():
    symbols_names = cPickle.load(open('PSE_LISTED_STOCKS_SYMBOLS_NAMES.dict'))
    access_site = raw_input("Please input the url for the site that you want to access: ")
    current_date = getCurrentDateInString()
    htmlOpener = getLoginAccess(access_site)

    symbols = sorted(symbols_names.keys())

    for symbol in symbols:
        print "Processing data for: %s" % symbol.upper()
        response = htmlOpener.open('https://www.philstocks.ph/Infinity/Transactions.cshtml?Symbol=%s' % symbol.upper())
        data = response.read()

        final_data = trimNuisancePartFromResponse(data)

        file_name = './%s/%s_%s.htm' % (symbol.upper(), symbol.upper(), current_date)
        if not os.path.isdir(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))

        f = file(file_name, 'w')
        f.write(final_data)
        f.close()

        time.sleep(0.2)

if __name__ == '__main__':
    main()
