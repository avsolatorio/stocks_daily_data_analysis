#-------------------------------------------------------------------------------
# Name:        philstocksDailyTransactionsDataParser.py
# Purpose:
#
# Author:      avsolatorio
#
# Created:     04/06/2014
# Copyright:   (c) avsolatorio 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import cPickle
import datetime
import re
import sys


def createReferenceTime():
    reference = datetime.datetime.now()
    reference = reference.replace(1, 1, 1, 9, 30, 0, 0)

    return reference

def returnFormattedTransactionTime(hour, minute, second):
    formattedTime = datetime.datetime.now()
    formattedTime = formattedTime.replace(1, 1, 1, hour, minute, second, 0)

    return formattedTime

def parseTransactionTimeToSeconds(transactionTime):
    returnTime = 0
    actualTime, indicator = transactionTime.split(' ')

    if 'AM' == indicator:
        hour, minute, second = map(lambda x: int(x), actualTime.split(':'))
        returnTime = returnFormattedTransactionTime(hour, minute, second) - createReferenceTime() #Calibrate time to start at 0
    else:
        hour, minute, second = map(lambda x: int(x), actualTime.split(':'))
        returnTime = returnFormattedTransactionTime(hour + 12, minute, second) - createReferenceTime() #Calibrate time to start at 0

    return returnTime.total_seconds()


def getTransactionPriceFromTransactionData(transactionData):
    pattern = '<span class="trnPrice">[\w\W]*?\n'
    M = re.findall(pattern, transactionData)

    return float(M[0].strip('\n').split('>')[-1])

def getTransactionVolumeFromTransactionData(transactionData):
    pattern = '<span class="trnVolume">[\w\W]*?\n'
    M = re.findall(pattern, transactionData)

    return float(''.join(M[0].strip('\n').split('>')[-1].split(',')))

def getTransactionTimeFromTransactionData(transactionData):
    pattern = '<span class="trnTime">[\w\W]*?\n'
    M = re.findall(pattern, transactionData)

    return parseTransactionTimeToSeconds(M[0].strip('\n').split('>')[-1])

def getTransactionBuyerFromTransactionData(transactionData):
    pattern = '<span class="trnBuyerSeller">[\w\W]*?</span>'
    M = re.findall(pattern, transactionData)

    return M[0].strip('</span>').split('>')[-1]

def getTransactionSellerFromTransactionData(transactionData):
    pattern = '<td style="border-right: 0px;"><span class="trnBuyerSeller">[\w\W]*?\n'
    M = re.findall(pattern, transactionData)

    return M[0].strip('\n').split('>')[-1]

def readMainDataFromFile(fname):
    try:
        rawData = open(fname).read()
    except:
        raise ValueError

    return rawData

def getListOfIndividualTransactionsFromData(data):
    pattern = '                    <tr>[\w\W]*?</tr>'
    M = re.findall(pattern, data)

    return M

def main():
    if len(sys.argv) == 2:
        if '.htm' in sys.argv[1]:
            completeData = []
            data = readMainDataFromFile(sys.argv[1])
            listOfTransactions = getListOfIndividualTransactionsFromData(data)

            for transactionData in listOfTransactions:
                transactionSummary = [getTransactionTimeFromTransactionData(transactionData),
                                        getTransactionPriceFromTransactionData(transactionData),
                                        getTransactionVolumeFromTransactionData(transactionData),
                                        getTransactionBuyerFromTransactionData(transactionData),
                                        getTransactionSellerFromTransactionData(transactionData)]
                completeData.append(transactionSummary)

            return sorted(completeData)
        else:
            print "Please input a valid raw data file from Philstocks transaction page."
    else:
        print "Please provide path for raw data file."

if __name__ == '__main__':
    completeData = main()
    brokers_buying = {}
    brokers_selling = {}

    for data in completeData:
        tTime, tPrice, tVolume, tBuyer, tSeller = data
        try:
            brokers_buying[tBuyer].append((tTime, tPrice, tVolume))
        except KeyError:
            brokers_buying[tBuyer] = [(tTime, tPrice, tVolume)]

        try:
            brokers_selling[tSeller].append((tTime, tPrice, tVolume))
        except KeyError:
            brokers_selling[tSeller] = [(tTime, tPrice, tVolume)]

    print brokers_buying
    print '--------------'
    print brokers_selling
    print '\n'
    print len(brokers_buying.keys())
    cPickle.dump(brokers_buying, file('brokers_buying.dict', 'w'))
    cPickle.dump(brokers_selling, file('brokers_selling.dict', 'w'))