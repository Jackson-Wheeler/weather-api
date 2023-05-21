from time import sleep

import pandas as pd
import json
import os
import sys
import pymysql
from pymysql import Error
from common import *
ssh_tunnel = True

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
        
    def loadStudents(self, gn: int):
        if self.check_conn():
            stu_df = pd.DataFrame
            if (gn is None):
                sqlStr = "SELECT * FROM cse191.students ORDER BY groupnumber"
            else:
                sqlStr = "SELECT * FROM cse191.students WHERE groupnumber={0} ORDER BY groupnumber".format(gn)
            print(sqlStr)
            cursor = self.db.cursor()
            result = None
            try:
                cursor.execute(sqlStr)
                result = cursor.fetchall()
                # print(result)
                stu_df = pd.DataFrame.from_dict(result) 
                stu_df.columns=["id","name","email","groupnumber","groupname"]
                # print(stu_df)
            except Error as e:
                print(f"The error '{e}' occurred")

            return stu_df

    def loadDevices(self, gn: int):
        if self.check_conn():
            dev_df = pd.DataFrame
            if (gn is None):
                sqlStr = "SELECT * FROM cse191.devices ORDER BY groupnumber"
            else:
                sqlStr = "SELECT * FROM cse191.devices WHERE groupnumber={0} ORDER BY groupnumber".format(gn)
            print(sqlStr)
            cursor = self.db.cursor()
            result = None
            try:
                cursor.execute(sqlStr)
                result = cursor.fetchall()
                # print(result)
                dev_df = pd.DataFrame.from_dict(result) 
                dev_df.columns=["device_id","mac","lastseen_ts","last_rssi","groupname", "location", "lang", "long", "color", "groupnumber"]
                # print(dev_df)
            except Error as e:
                print(f"The error '{e}' occurred")

            return dev_df
        
    def loadBleLogs(self, gn: int):
        if self.check_conn():
            ble_logs_df = pd.DataFrame
            if (gn is None):
                sqlStr = "SELECT * FROM cse191.ble_logs"
            else:
                sqlStr = "SELECT * FROM cse191.ble_logs WHERE groupnumber={0}".format(gn)
            print(sqlStr)
            cursor = self.db.cursor()
            result = None
            try:
                cursor.execute(sqlStr)
                result = cursor.fetchall()
                # print(result)
                ble_logs_df = pd.DataFrame.from_dict(result) 
                ble_logs_df.columns=["log_id","device_mac","ble_rssi","ble_mac","groupname", "log_ts", "ble_count"]
                # print(ble_logs_df)
            except Error as e:
                print(f"The error '{e}' occurred")

            return ble_logs_df
        

            
        

    def logDevices(self, data: LogInfo):
        if self.check_conn():
            groupname = "threefoldCord"
            dev_df = pd.DataFrame
            # For each BLEDevice, insert it into DB's ble_logs table
            for device in data.devices:
                sqlStr = "INSERT INTO cse191.ble_logs (device_mac, ble_rssi, ble_mac, groupname) VALUES ('{0}', '{1}', '{2}', '{3}');".format(data.espmac, device.rssi, device.mac, groupname)
                print(sqlStr)
                cursor = self.db.cursor()
                try:
                    cursor.execute(sqlStr)
                    result = cursor.fetchall()
                    self.db.commit()
                    print(result)
                except Error as e:
                    print(f"The error '{e}' occurred")
                    return False
            return True
        # if check_conn() fails
        else: return False

    