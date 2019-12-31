import pypyodbc
from flask import Flask,jsonify,request,make_response,logging
import jwt
import json
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super_safe_secretasas33323232as23as2a3s2s3a2s3a2s32a3s'

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'msg': 'token req', }),401

        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
        except:
          return jsonify({'msg':'token is not valid',}),401
        return f(data,*args,**kwargs)
    return decorated




@app.route('/Creater')
def Creater():
    return jsonify({'creater': 'Rishab Aggarwal','Email': 'Rishabaggarwal247@gmail.com' } ),200
@app.route('/')
def Start():
    return jsonify({'msg': 'Welcome!' } ),200
@app.route('/About')
def About():
    return jsonify({'About': 'STUFFFF' } ),200


@app.route('/Verify',methods=['GET'])
@token_required
def Verify(data):
    query = "SELECT  [Status] FROM [dbo].[Status]where Euid = '"+data['user'] +"' "
    result = run_query(query)
    print(result[0][0])
    return jsonify({'Status':result[0][0]  }),200


@app.route('/login')
def login():
    auth = request.authorization
    print(auth)
    query1  = "SELECT [Password] FROM [dbo].[user_info] WHERE Euid = '"+auth.username+"'"
    query2 = "SELECT  [HOD],[Hod_Department] FROM [dbo].[Status]where Euid = '"+auth.username +"' "
    print(query1)
    result = login_query(query1,query2)
    print(result[0])
    if auth and auth.password ==result[0]:
        token = jwt.encode({'user': auth.username,'HOD': result[1],
                            'hod_department': result[2],
                            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60)},app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response({'msg':'Login req'},401,{'msg':'Login req'})



@app.route('/register', methods=['POST'])
def register():
    data = request.get_data().decode("utf-8")
    data = json.loads(data)
    query1 = "INSERT INTO [dbo].[user_info] VALUES ("
    query1 = query1+ "'"+data['Euid']+"',"
    query1 = query1+ "'"+data['Name']+"',"
    query1 = query1+ "'"+data['Email']+"',"
    query1 = query1+ "'"+data['Password']+"',"
    query1 = query1+ "'"+data['Phone_No']+"',"
    query1 = query1+ "'"+data['Department_Name']+"',"
    query1 = query1+ "'"+data['DOJ']+"',"
    query1 = query1+ "'"+data['Qualifications']+"',"
    query1 = query1+ "'"+data['University']+"',"
    query1 = query1+ "'"+data['DOB']+"'"+");"

    query2 = "INSERT INTO [dbo].[Status] VALUES ("
    query2 = query2+ "'"+data['Euid']+"',"
    query2 = query2+ "0,0,"
    query2 = query2+ "'"+data['Name']+"',"
    query2 = query2+ "'"+data['Hod_Department']+"');"
    print(query2)
    return register_query(query1,query2)

















def run_query(query1):
    try:
        connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                      'Server=tcp:timsserver1.database.windows.net,1433;'
                                      'Database=TIMS;'
                                      'Uid=timsadmin;Pwd=Rishab@12;')
        try:

            cursor = connection.cursor()
            cursor.execute(query1)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return  result
        except Exception as e:
            connection.close()
            return str(e)
    except Exception as e:
        return  str(e)




def login_query(query1,query2):
    try:
        connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                      'Server=tcp:timsserver1.database.windows.net,1433;'
                                      'Database=TIMS;'
                                      'Uid=timsadmin;Pwd=Rishab@12;')
        try:

            cursor = connection.cursor()
            cursor.execute(query1)
            result = cursor.fetchone()
            cursor.execute(query2)
            result1 =cursor.fetchone()
            cursor.close()
            connection.close()
            a = [result[0],result1[0],result1[1]]
            return  a
        except Exception as e:
            connection.close()
            return str(e)
    except Exception as e:
        return  str(e)



def register_query(query1,query2):
    try:
        connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                      'Server=tcp:timsserver1.database.windows.net,1433;'
                                      'Database=TIMS;'
                                      'Uid=timsadmin;Pwd=Rishab@12;')
        try:

            cursor = connection.cursor()
            cursor.execute(query1)
            cursor.execute(query2)
            cursor.commit()
            connection.close()
            return jsonify({'msg': 'inserted', }), 200
        except Exception as e:
            connection.close()
            return jsonify({'msg': str(e)}), 401
    except Exception as e:
        return jsonify({'msg': str(e)}), 401


if __name__ == '__main__':


    app.run(host='https://apitims.azurewebsites.net')
