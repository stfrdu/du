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
class dataGrapher:
    #initialize method to hold all major class attributes
    def __init__(self, symbol):
        self.symbol = symbol

    #method to retrieve data and graph
    def jsonShareUpdate(symbol):
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

        #select jsonData close values
        cursor.execute('SELECT Date FROM jsonData WHERE Symbol = "' + symbol + '"')
        data = cursor.fetchall()

        #format and store dates in list
        for row in data:
            row = str(row)
            row = row.replace('(','')
            row = row.replace(',','')
            row = row.replace(')','')
            row = row.replace('\'','')
            dates.append(datetime.strptime(row, '%Y-%m-%d %H:%M:%S'))
        
        #declare variables to hold relevant data and push them into graph
        value = totVal
        date = matplotlib.dates.date2num(dates)
        name = symbol
        plt.plot_date(date,value,linestyle='solid',label=name, marker="None")

        #close database connection
        connection.close()