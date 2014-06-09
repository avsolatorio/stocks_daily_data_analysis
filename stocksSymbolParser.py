#-------------------------------------------------------------------------------
# Name:        stocksSymbolParser.py
# Purpose:     Parse symbols and names of listed stocks in PSE from '.htm' file.
#
# Author:      avsolatorio
#
# Created:     10/06/2014
# Copyright:   (c) avsolatorio 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import cPickle
import re
import sys


def getStockName(stockData):
    pattern = '<span class="guideTableStockName">[\w\W]*?</span>'
    M = re.findall(pattern, stockData)

    return M[0].strip('</span>').split('>')[-1]

def getStockSymbol(stockData):
    pattern = '<span class="guideTableStockSymbol">[\w\W]*?\n'
    M = re.findall(pattern, stockData)

    return M[0].strip('\n').split('>')[-1]

def getRawData(file_name):
    try:
        source = open(file_name)
        raw_data = source.read()
        source.close()
    except IOError:
        raw_data = None

    return raw_data

def main():
    if len(sys.argv) > 1:
        count_of_files_provided = len(sys.argv) - 1     #Use this to check if there is no valid file name passed in the arguments list
        symbol_name_dict = {}

        for fname in sys.argv[1:]:
            if '.htm' not in fname:
                count_of_files_provided -= 1
                print fname
                continue

            raw_data = getRawData(fname)

            if not raw_data:
                count_of_files_provided -= 1
                print fname
                continue

            for tbody in re.findall('<tbody>[\w\W]*?</tbody>', raw_data):
                for tr in re.findall('<tr>[\w\W]*?</tr>', tbody):
                    symbol = getStockSymbol(tr)
                    name = getStockName(tr)
                    symbol_name_dict[symbol] = name

        if not count_of_files_provided:
            print "No valid raw data was provided in the arguments."
        else:
            cPickle.dump(symbol_name_dict, file("PSE_LISTED_STOCKS_SYMBOLS_NAMES.dict", "w"))
    else:
        print "Please provide path for raw data file."

if __name__ == '__main__':
    main()
