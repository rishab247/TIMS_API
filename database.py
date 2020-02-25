import pypyodbc

import re

connection = None
i = 0
try:

    connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                  'Server=tcp:timsserver1.database.windows.net,1433;'
                                  'Database=TIMS;'
                                  'Uid=timsadmin;Pwd=Rishab@12;')


except Exception as e:
    print(str(e))


def retry():
    try:
        global connection
        connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                      'Server=tcp:timsserver1.database.windows.net,1433;'
                                      'Database=TIMS;'
                                      'Uid=timsadmin;Pwd=Rishab@12;')
        return connection

    except Exception as e:
        print(str(e))


def getconnection():
    try:

        if connection.connected:
            return connection
        else:
            return retry()
    except Exception as e:
        print(str(e))


def query(query1, fetch, list):
    connection = getconnection()
    global i
    print(query1)
    print(list)
    try:
        cursor = connection.cursor()
        cursor.execute(query1, list)
        if fetch == 0:
            result = cursor.fetchone()
            connection.commit()
            cursor.close()
            return result
        elif fetch == 1:
            result = cursor.fetchall()
            connection.commit()
            cursor.close()

            return result
        else:
            connection.commit()
            cursor.close()
            return 'Finished'
        i=0
    except Exception as e:

        i = i+ 1
        print(str(i)+"12")
        print('exeption'+str(e))
        if ((i %2)!=0):
            retry()
            query(query1, fetch, list)

def query1(query1, fetch):
    connection = getconnection()
    global i
    print(query1)
    try:

        cursor = connection.cursor()
        cursor.execute(query1)
        if fetch == 0:
            result = cursor.fetchone()
            connection.commit()
            cursor.close()
            # print("result"+str(result))

            return result
        elif fetch == 1:
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
            # print("result"+str(result))

            return result
        else:
            connection.commit()
            cursor.close()
            return 'Finished'
        i=0
    except Exception as e:

        i = i+ 1
        print(str(i)+"12")
        print(str(e))
        if ((i %2)!=0):
            retry()
            query(query1, fetch, list)



def check(string):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if (regex.search(string) == None):
        return True

    else:
        return False


def Email_check(string):
    regex = re.compile('[_!#$%^&*()<>?/\|}{~:]')
    if (regex.search(string) == None):
        return True

    else:
        return False

#
# class DecimalEncoder(json.JSONEncoder):
#     def _iterencode(self, o, markers=None):
#         if isinstance(o, decimal.Decimal):
#
#             return (str(o) for o in [o])
#         return super(DecimalEncoder, self)._iterencode(o, markers)
