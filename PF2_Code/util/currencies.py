#
# ===========================================================================================
# Currencies exchange rates
# ===========================================================================================
# ===========================================================================================


# System libraries
import requests
import json
import time  

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


# App Specific libraries
from data_modules import DB_Util


# ===========================================================================================

# Currencies Exchange Class
class Currencies():
    def __init__(self, parent=None):
        self.db = DB_Util()
        self.currDate = time.strftime('%Y-%m-%d') # current date
        #self.db = DB_Util(dbVersion='Test')

        
    def updateCurrencies(self):
        
        lastDate = self.getLastRateDate() # last date that curencies were updated
        # if currencies were not yet updated today, update
        if lastDate < self.currDate:
            self.currList = self.getCurrenciesList()
            #self.rates = {'EUR': 1.0, 'USD': 1.0978334257343134, 'MKD': 61.620111210526034, 'GBP': 0.8487405106023264, 'HRK': 7.457089533805036, 'VND': 25512.00206392684, 'THB': 34.17580155562997, 'IDR': 14979.937094144707}
            self.rates = self.getRates()
            self.updateRegCurrencies()
            self.updateCryptoCurrencies()

    # get last date that curencies were updated
    def getLastRateDate(self):  
        query = "SELECT MAX(RATE_DATE) FROM REG_CURRENCY"
        data = self.db.getData(query).fetchone()
        lastDate = data[0]

        lastDate = lastDate.strftime('%Y-%m-%d')

        return lastDate

    # get currencies used by the Personal Finances App
    def getCurrenciesList(self):
        query_currency = "SELECT curr_code FROM REG_CURRENCY"
        data_currency = self.db.getData(query_currency)
        
        currList = []
        for row in data_currency:
            currList.append(row[0])
           
        return currList

    # get live currency rates
    def getRates (self):
        ratesUSD = {}
        ratesEUR = {}
        params = {}

        url = 'http://api.currencylayer.com/live'
        params['access_key'] = 'df080fbd6c0040d3f079496b64a06ed4'
        params['currencies'] = ', '.join(map(str, self.currList)) 
        params['format'] = 1
        
        data = requests.get(url, params)
        ratesList = data.json().get('quotes')
        
        for key in ratesList.keys():
            #print(ratesList.get(key))              
            ratesUSD[key[3:]] = ratesList.get(key)
        
        eur = ratesUSD['EUR']
        for key in ratesUSD.keys():
            # exception for EUR/USD - Add USD to the list
            if key == 'EUR':
                ratesEUR['USD'] = 1 / eur
            
            ratesEUR[key] = ratesUSD.get(key) / eur

        return ratesEUR
        
    # update currencies        
    def updateRegCurrencies (self):
        # check old allocation sum
        query = "SELECT SUM(VALUE) FROM MONEY_ALLOCATION"
        data = self.db.getData(query).fetchone()
        oldAllocationSum = round(data[0], 2)
        
        for key in self.rates.keys():
            currCode = key
            currRate = self.rates.get(key)

            update_stmt = "UPDATE REG_CURRENCY SET CURR_RATE = " + str(currRate) + ", RATE_DATE = '" + str(self.currDate) + "' WHERE CURR_CODE = '" + str(currCode)+ "'"
            self.db.executeDDL(ddl=update_stmt)

        # check new allocation sum
        query = "SELECT SUM(VALUE) FROM MONEY_ALLOCATION"
        data = self.db.getData(query).fetchone()
        newAllocationSum = round(data[0], 2)
        
        # update currency conversion difference for monwy check purpose
        currencyCheckSum = oldAllocationSum - newAllocationSum

        update_stmt = "UPDATE REG_SYS_VARIABLES SET CURRENCY_CHECK_SUM = CURRENCY_CHECK_SUM + " + str(currencyCheckSum)
        self.db.executeDDL(ddl=update_stmt)
        
        self.db.saveData() 
    
    def getCryptoRate(self, cryptoCode):
        
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
        'start':'1',
        'limit':'5000',
        'convert':'EUR'
        }
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'fbbbd76f-37b8-4cee-9a4a-b396f5b0b48b',
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            dataAll = json.loads(response.text)
            dataCurrencies = dataAll['data']
            data = dataCurrencies[cryptoCode]
            quote = data['quote']
            crypto = quote['EUR']
            priceEUR = crypto['price']

            return priceEUR

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)  
            return 0

    
    def updateCryptoCurrencies(self):

        cryptoCode = 'BTC'
        cryptoValue = self.getCryptoRate(0)
        update_stmt = "UPDATE REG_CURRENCY SET CURR_RATE = " + str(cryptoValue) + ", RATE_DATE = '" + str(self.currDate) + "' WHERE CURR_CODE = '" + str(cryptoCode)+ "'"
        self.db.executeDDL(ddl=update_stmt)
        

        cryptoCode = 'ETH'
        cryptoValue = self.getCryptoRate(1)
        update_stmt = "UPDATE REG_CURRENCY SET CURR_RATE = " + str(cryptoValue) + ", RATE_DATE = '" + str(self.currDate) + "' WHERE CURR_CODE = '" + str(cryptoCode)+ "'"
        self.db.executeDDL(ddl=update_stmt)
        

        self.db.saveData()