from time import sleep
from datetime import datetime

import pandas as pd
import json
import os
import sys
import pymysql
from pymysql import Error
from common import *


ssh_tunnel = False

groupname = "3foldCord"
zipcode = "01000"

'''
for remote access - add HOSTNAME=localhost to env  
ssh -L 8676:127.0.0.1:3306 group03@cse191.ucsd.edu
'''
class dbClass:

    def __init__(self, type="JSON"):
        self.outType = type
        # AMAZON CLOUD - AWS DB Cluster
        print("connect to main DB")
        self.servername = "127.0.0.1"
        self.username = "root"
        self.password = "iotiot"
        self.dbname = "cse191"
        self.port = 3306
        # if os.getenv('HOSTNAME') == "localhost":
        if ssh_tunnel:
            print("connect local ssh tunnel")
            self.port = 8676

        self.reconnect()

    def check_conn(self):

        # test connection
        try:
            if self.db.cursor().execute("SELECT now()") == 0:
                return self.reconnect()
            else:
                print("DB connection OK\n")
                return True
        except:
            print("Unexpected exception occurred: ", sys.exc_info())
            return self.reconnect()

    def reconnect(self):

        # try to connect 5 times
        retry = 5
        while retry > 0:
            try:
                print("connecting to DB...")
                self.db = pymysql.connect(
                    host=self.servername,
                    user=self.username,
                    password=self.password,
                    database=self.dbname,
                    port=self.port
                )
                retry = 0
                return True
            except:
                print("Unexpected exception occurred: ", sys.exc_info())
                retry -= 1
                if retry > 0:
                    print("retry\n")
                    sleep(2)
                else:
                    exit(-1)

        print("Success\n")

    def loadWeather(self, gn):
        if self.check_conn():
            weather_df = pd.DataFrame
            if (gn is None):
                sqlStr = "SELECT * FROM cse191.forecast"
            else:
                sqlStr = "SELECT * FROM cse191.forecast WHERE groupname={0}".format(gn)
            print(sqlStr)
            cursor = self.db.cursor()
            result = None
            try:
                cursor.execute(sqlStr)
                result = cursor.fetchall()
                weather_df = pd.DataFrame.from_dict(result)
                weather_df.columns=["forecast_id", "temperature", "humidity", "min_temp", "max_temp", "forecast_ts",  "groupname", "sunrise", "sunset", "zipcode"]
            except Error as e:
                print(f"The error '{e}' occured")

            return weather_df
        

    # add JSON of weather data to DB
    def add_to_db(self, json):
        if self.check_conn():
            # convert time stamps to date time format
            forecast_dt = datetime.fromtimestamp(json["dt"]).strftime('%Y-%m-%d %H:%M:%S')
            sunrise_dt = datetime.fromtimestamp(json["sys"]["sunrise"])
            sunset_dt = datetime.fromtimestamp(json["sys"]["sunset"])
            current_dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            print("Adding data to DB - currtime: " + current_dt)
            # Make SQL String
            sqlStr = "INSERT INTO cse191.forecast (temperature, humidity, min_temp, max_temp, forecast_ts, groupname, sunrise, sunset, zipcode) "
            sqlStr += "VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}', '{8}');".format(json["main"]["temp"], json["main"]["humidity"], json["main"]["temp_min"], json["main"]["temp_max"], forecast_dt, groupname, sunrise_dt, sunset_dt, zipcode)

            # execute sql statement
            cursor = self.db.cursor()
            try:
                cursor.execute(sqlStr)
                result = cursor.fetchall()
                self.db.commit()
                # print(result)
            except Error as e:
                print(f"The error '{e}' occurred")
                return False
            return True
        # if connection fails
        else: 
            print("Connection to Database failed... returning false")
            return False
