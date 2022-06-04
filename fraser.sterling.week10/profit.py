"""
Sterling Fraser
ICT 4370-1
05/22/2022
Week 8
Description:
This module is responsible for pulling in data from databases,
storing it, and plotting it on a graph 
"""

try:
    #import supporting modules
    import workspaceURL as url
    import sqlite3 as sql
    import pandas as pd
    import matplotlib
    import matplotlib.pyplot as plt
    from datetime import datetime
except ModuleNotFoundError:
    print("Failed to import modules")

#declare class holding data retrieval and graphing methods
class ProfitCalculator:
    #initialize method to hold all major class attributes
    def __init__(self, symbol):
        self.symbol = symbol

    #method to retrieve data and graph
    def profitTable(symbol):
        try:
            #connect to database
            connection = sql.connect(url.workspace + "\stockAssgmt.db")
            cursor = connection.cursor()
        except:
            print('failed to connect to database')
            
        #create empty lists to hold data
        closeVals = []
        quantVals = ""
        totVal = []
        dates = []
        purchaseVals = ""
        profitVals = []
        taxBurd = []
        today = datetime.now()

        #select jsonData close values
        cursor.execute('SELECT Close FROM jsonData WHERE Symbol = "' + symbol + '"')
        data = cursor.fetchall()
        #format and store data in list
        for row in data:
            row = str(row)
            row = row.replace('(','')
            row = row.replace(',','')
            row = row.replace(')','')
            closeVals.append(float(row))
        
        # select stock quantity values
        cursor.execute('SELECT NO_SHARES FROM Stocks WHERE SYMBOL = "' + symbol + '"')
        data2 = cursor.fetchall()
        #format and store data in list
        for row in data2:
            row = str(row)
            row = row.replace('(','')
            row = row.replace(',','')
            row = row.replace(')','')
            quantVals = float(row)
        
        #calculate and store total value of stocks
        for i in closeVals:
            i = float(i) * float(quantVals)
            totVal.append(round(i,2))

        #select Stocks purchase price
        cursor.execute('SELECT PURCHASE_PRICE FROM Stocks WHERE Symbol = "' + symbol + '"')
        data3 = cursor.fetchall()
        #format and store purchase price in list
        for row in data3:
            row = str(row)
            row = row.replace('(','')
            row = row.replace(',','')
            row = row.replace(')','')
            purchaseVals = float(row)

        #select jsonData date values
        cursor.execute('SELECT Date FROM jsonData WHERE Symbol = "' + symbol + '"')
        data4 = cursor.fetchall()
        #format and store dates in list
        for row in data4:
            row = str(row)
            row = row.replace('(','')
            row = row.replace(',','')
            row = row.replace(')','')
            row = row.replace('\'','')
            dates.append(datetime.strptime(row, '%Y-%m-%d %H:%M:%S'))
        
        #calculate and store profit of stocks
        count = 0
        for i in totVal:
            i = float(totVal[count]) - float(quantVals) * float(purchaseVals)
            profitVals.append(round(i,2))
            count = count + 1
        
        #calculate and store tax burden of realized gains if sold
        count = 0
        for i in profitVals:
            # date2 = datetime.strptime(dates[count], "%Y-%m-%d")
            date2 = (dates[count])
            timedelta = (today-date2)
            # short term capital gains (if sold within 365 days of purchase)
            if timedelta.days <= 365:
                if i <= 10275:
                    # 10% bracket
                    taxBurd.append(i*.10)
                elif i >=10276 and i <=41775:
                    # 12% bracket
                    taxBurd.append((10275*.1)+((i-10275)*.12))
                elif i >=41776 and i <=89075:
                    # 22% bracket
                    taxBurd.append((10275*.1)+((41775-10275)*.12)+((i-41775)*.22))
                elif i >=89076 and i <=170050:
                    # 24% bracket
                    taxBurd.append((10275*.1)+((41775-10275)*.12)+((89075-41775)*.22)+((i-89075)*.24))
                elif i >=170051 and i <=215950:
                    # 32% bracket
                    taxBurd.append((10275*.1)+((41775-10275)*.12)+((89075-41775)*.22)+((170050-89075)*.24)+((i-170050)*.32))
                elif i >=215951 and i <=539900:
                    # 35% bracket
                    taxBurd.append((10275*.1)+((41775-10275)*.12)+((89075-41775)*.22)+((170050-89075)*.24)+((215950-170050)*.32)+((i-215950)*.35))
                else:
                    # 37% bracket
                    taxBurd.append((10275*.1)+((41775-10275)*.12)+((89075-41775)*.22)+((170050-89075)*.24)+((215950-170050)*.32)+((539900-215950)*.35)+((i-539900)*.37))
            # long term capital gains (if sold over 365 days from purchase)
            else: 
                if i <= 41675:
                    # 0% bracket
                    taxBurd.append(0)
                elif i >= 41676 and i <= 459750:
                    # 15% bracket
                    taxBurd.append((i-41676)*.15)
                else:
                    # 20% bracket
                    taxBurd.append(((459750-41676)*.15)+((i-459750)*.2))
            count = count + 1

        #create dataframe and populate it with all data, then push into database
        dataLists = {'Symbol':symbol, "Date":dates, "Value":totVal, "Profit/Loss":profitVals, "Tax Burden":taxBurd}
        df = pd.DataFrame(dataLists)
        df.to_sql(name='ProfitAndTax', con=connection, if_exists='append')

        #close database connection
        connection.close()
