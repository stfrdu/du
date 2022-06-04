"""
Sterling Fraser
ICT 4370-1
04/26/2022
Week 5 Stock/Bond Lists
Description:
The core of the python program that calls in all relevant modules and runs primary functions
"""

"""
====  FILE PATH  ====
If you need to change the workspace file path, go to the workspaceURL module and update it there. 
This updates everything globally.
"""
try:
    # import universal workspace url
    import workspaceURL as url

    # import supporting modules
    import csvReader as csvr
    import jsonReader as jsonr
    import grapher as gph
    import sqlite3 as sql
    import pandas as pd
    import profit as profit
except ModuleNotFoundError:
    print("Failed to import modules")
    
# call in methods to populate the database with json file and other investor data from csv files
jsonr.jsonRead.readInJson()
csvr.sbiCSV.stockDataPopulate()
csvr.sbiCSV.bondDataPopulate()
csvr.sbiCSV.investorDataPopulate()

#connect to populated database
connection = sql.connect(url.workspace + "\stockAssgmt.db")
cursor = connection.cursor()

#create for loop to retrieve stock Symbols and populate a list
symbols = []
cursor.execute('SELECT SYMBOL FROM Stocks')
stockSymbols = cursor.fetchall()
for row in stockSymbols:
    row = str(row)
    row = row.replace('(','')
    row = row.replace(',','')
    row = row.replace(')','')
    row = row.replace('\'','')
    symbols.append(row)

#define graph dimensions
gph.plt.figure(figsize=(9,6))

#use stock list to call grapher method for all stock Symbols
for symbol in symbols:
    gph.dataGrapher.jsonShareUpdate(symbol)

# use stock list to loop and populate tax burden table
cursor.execute('DROP TABLE IF EXISTS ProfitAndTax')
for symbol in symbols:
    profit.ProfitCalculator.profitTable(symbol)

#declare graph details and show graph of all data
gph.plt.legend()
gph.plt.xlabel('Date')
gph.plt.ylabel('Value')

# plotting a line plot
gph.plt.savefig('simplePlot.png')