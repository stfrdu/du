"""
Sterling Fraser
ICT 4370-1
04/26/2022
Week 5 Stock/Bond Lists
Description:
A program that imports csv data and loads it into a database
"""

#import supporting modules
try:
    import workspaceURL as url
    from distutils.log import error
    import sqlite3 as sql
    import pandas as pd
    import csv
except ModuleNotFoundError:
    print("Failed to import modules")

#declare class to hold methods to populate database with csv files
class sbiCSV:
    #define method to populate stock data      
    def stockDataPopulate():
        try:
            # connect to database
            connection = sql.connect(url.workspace + "\stockAssgmt.db")
            cursor = connection.cursor()
        except:
            print('failed to connect to database')

        try:
            #declare variables to hold pathways for files read into program
            text_file1 = url.workspace + '\\' + 'Lesson6_Data_Stocks.csv'
        except FileNotFoundError:
            print("Stock Data not found.")    
        #load csvs into dataframes
        df = pd.read_csv(text_file1)
        #establish lists to hold IDs
        stockID = []
        investorIDS = []

        #generate ids for stocks using loop dependent on how many rows exist
        for index, row in df.iterrows():
            stockID.append('STK' + str(index))
            investorIDS.append('INV1')

        #add ids to stock dataframe
        df['StockID'] = stockID
        df['InvestorID'] = investorIDS

        #feed modified csv data into the database
        df.to_sql('Stocks',connection,if_exists='replace')

        #close database connection
        connection.close()

    def bondDataPopulate():
        try:
            #connect to database
            connection = sql.connect(url.workspace + "\stockAssgmt.db")
            cursor = connection.cursor()
        except:
            print('failed to connect to database')
            
        try:
            #declare variables to hold pathways for files read into program
            text_file2 = url.workspace + '\\' + 'Lesson6_Data_Bonds.csv'
        except FileNotFoundError:
            print("Bond Data not found.")
        #load csvs into dataframes
        df2 = pd.read_csv(text_file2)
        #establish lists to hold IDs
        bondID = []
        investorIDB = []

        #generate ids for bonds using loop dependent on how many rows exist
        for index, row in df2.iterrows():
            bondID.append('BND' + str(index))
            investorIDB.append('INV1')

        #add ids to bond dataframe
        df2['BondID'] = bondID
        df2['InvestorID'] = investorIDB

        #feed modified csv data into the database
        df2.to_sql('Bonds',connection,if_exists='replace')

        #close database
        connection.close()

    def investorDataPopulate():
        try:
            #connect to database
            connection = sql.connect(url.workspace + "\stockAssgmt.db")
            cursor = connection.cursor()
        except:
            print('failed to connect to database')

        try:
            #declare variables to hold pathways for files read into program
            text_file3 = url.workspace + '\\' + 'Lesson6_Data_Investors.csv'
        except FileNotFoundError:
            print("Investor Data not found.")
        #load csvs into dataframes
        df3 = pd.read_csv(text_file3)

        #feed modified csv data into the database
        df3.to_sql('Investors',connection, if_exists='replace')

        #close database connection
        connection.close()

