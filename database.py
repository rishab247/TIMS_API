import pypyodbc
from flask import Flask,jsonify,request,make_response,logging
import jwt
import json
import datetime



try:
        connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                      'Server=tcp:timsserver1.database.windows.net,1433;'
                                      'Database=TIMS;'
                                      'Uid=timsadmin;Pwd=Rishab@12;')


except Exception as e:
          print(str(e))

def retry():
    try:
        connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                      'Server=tcp:timsserver1.database.windows.net,1433;'
                                      'Database=TIMS;'
                                      'Uid=timsadmin;Pwd=Rishab@12;')
        return connection

    except Exception as e:
        print(str(e))

def getconnection():
    if connection!=None:
        return connection
    else:
       retry()


def query(query1,fetch):
        try:

            cursor = connection.cursor()
            cursor.execute(query1)
            if fetch==0:
                result = cursor.fetchone()
                connection.commit()
                cursor.close()
                return result
            elif fetch==1:
                result = cursor.fetchall()
                connection.commit()
                cursor.close()
                return result
            else:
                connection.commit()
                cursor.close()
                return 'Finished'

        except Exception as e:
            return str(e)

