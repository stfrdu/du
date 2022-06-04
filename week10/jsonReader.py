"""
Sterling Fraser
ICT 4370-1
04/26/2022
Week 5 Stock/Bond Lists
Description:
A program that imports JSON data and loads it into a database
"""

try: 
    import workspaceURL as url
    from cProfile import label
    import json
    from multiprocessing.sharedctypes import Value
    import sqlite3 as sql
    import pandas as pd
except ModuleNotFoundError:
    print("Failed to import modules")

class jsonRead:
    def readInJson():
        try: 
            #define where files are held
            filename = '\AllStocks.json'
            #add json file into dataframe using pandas
            df = pd.read_json(url.workspace + filename)
        except FileNotFoundError:
            print("JSON Data not found.")

        #establish connection to database
        try:
            connection = sql.connect(url.workspace + "\stockAssgmt.db")
            cursor = connection.cursor()
        except:
            print('failed to connect to database')

        #feed json data into the database into a table called jsonData
        df.to_sql('jsonData',connection, if_exists='replace')