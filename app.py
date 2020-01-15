import pypyodbc
from flask import Flask, jsonify, request, make_response, logging
import jwt
import json
import datetime
import database as db
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super_safe_67uy67uy54tre3we098uy6t5r1q2we345ty7u8io90secretasas33323232as23as2a3s2s3a2s3a2s32a3s'
# connection
try:
    connection = db.getconnection()
except:
    try:
        connection = db.getconnection()
    except Exception as e:
        print(str(e))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'msg': 'token req', }), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'msg': 'token is not valid', }), 401
        return f(data, *args, **kwargs)

    return decorated


@app.route('/Creater')
def Creater():
    return jsonify({'creater': 'Rishab Aggarwal', 'Email': 'Rishabaggarwal247@gmail.com', 'creater1': 'tushar tambi',
                    'Email1': 'tushartambi@gmail.com'}), 200


@app.route('/')
def Start():
    return jsonify({'msg': 'Hello World!'}), 200


@app.route('/About')
def About():
    return jsonify({'About': 'STUFFFF'}), 200

@app.route('/Alert')
def Alert():
    return jsonify({'msg': 'Alert!'}), 200



@app.route('/Verify', methods=['GET'])
@token_required
def Verify(data):

    query = "SELECT  [Status] FROM [dbo].[Status]where Euid = '" + data['user'] + "' "
    result = db.query(query, 0)
    return jsonify({'Status': result[0]}), 200


@app.route('/login')
def login():

        auth = request.authorization
        if auth is None:
            return make_response({'msg': 'Login req'}, 401, {'msg': 'Login req'})
        if auth.username == '' or auth.password == '':
            return make_response({'msg': 'Login req'}, 401, {'msg': 'Login req'})
        if not db.check(auth.username) or not db.check(auth.password):
            return make_response({'msg': 'Login req'}, 401, {'msg': 'Login req'})
        query1 = "SELECT [Password] FROM [dbo].[user_info] WHERE Euid = '" + auth.username + "'"
        query2 = "SELECT  [HOD],[Hod_Department] FROM [dbo].[Status]where Euid = '" + auth.username + "' "
        result = (db.query(query1, 0))
        result1 = (db.query(query2, 0))
        if result is None:
            return jsonify({'msg': 'incorrect username'}), 401
        if auth and auth.password == result[0]:
            token = jwt.encode({'user': auth.username, 'HOD': result1[0],
                                'hod_department': result1[1],
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                               app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('UTF-8')})
        return make_response({'msg': 'Login req'}, 401, {'msg': 'Login req'})



@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_data().decode("utf-8")
        data = json.loads(data)
        if not db.check(data['Euid']) or not db.check(data['Name'])or not db.Email_check(data['Email'])or not db.check(data['Password'])or \
                not db.check(data['Phone_No']) or not db.check(data['Department_Name']) or not db.check(data['DOJ']) or \
                not db.check(data['Qualifications']) or not db.check(data['University']) or not db.check(data['DOB'])or \
                not db.check(data['Hod_Department']):
            raise Exception
        query1 = "INSERT INTO [dbo].[user_info] VALUES ("
        query1 = query1 + "'" + data['Euid'] + "',"
        query1 = query1 + "'" + data['Name'] + "',"
        query1 = query1 + "'" + data['Email'] + "',"
        query1 = query1 + "'" + data['Password'] + "',"
        query1 = query1 + "'" + data['Phone_No'] + "',"
        query1 = query1 + "'" + data['Department_Name'] + "',"
        query1 = query1 + "'" + data['DOJ'] + "',"
        query1 = query1 + "'" + data['Qualifications'] + "',"
        query1 = query1 + "'" + data['University'] + "',"
        query1 = query1 + "'" + data['DOB'] + "'" + ");"
        query2 = "INSERT INTO [dbo].[Status] VALUES ("
        query2 = query2 + "'" + data['Euid'] + "',"
        query2 = query2 + "0,0,"
        query2 = query2 + "'" + data['Name'] + "',"
        query2 = query2 + "'" + data['Hod_Department'] + "');"
        result1 = (db.query(query1, 2))
        result2 = (db.query(query2, 2))
        if result1 == 'Finished' and result2 == 'Finished':
            return jsonify({'msg': 'inserted', }), 200
        return jsonify({'msg': result1 + '   ' + result2, }), 401
    except Exception as e:
        return jsonify({"msg": str(e)}),401


@app.route('/userdata', methods=['GET'])
@token_required
def userdata(data):
    query = "SELECT [Euid],[Name],[Email],[Phone_No],[Department_Name],[DOJ],[Qualifications],[University],[DOB] FROM [dbo].[user_info]where Euid = '" + data['user'] + "' "
    result = db.query(query, 0)
    print(result)
    return jsonify({'Status': (result)}), 200


@app.route('/user/List')
@token_required
def userpaperlist(data):
    # query = "SELECT  * FROM [dbo].[research_paper] where Euid = '" + data['user'] + "' "
    try:
        try:
            result = db.query("SELECT  * FROM [dbo].[Project_1] where Euid = '" + data['user'] + "' ", 1)
        except Exception as e:
            result  = "No data present"+str(e)
        try:
            result1 = db.query("SELECT  * FROM [dbo].[Publication] where Euid = '" + data['user'] + "' ", 1)
        except Exception as e:
            result1  = "No data present"+str(e)
        try:
            result2 = db.query("SELECT  * FROM [dbo].[Honors_and_Award] where Euid = '" + data['user'] + "' ", 1)
        except Exception as e:
            result2  = "No data present"+str(e)
        try:
            result3 = db.query("SELECT  * FROM [dbo].[Patent] where Euid = '" + data['user'] + "' ", 1)
        except Exception as e:
            result3  = "No data present"+str(e)
        return jsonify({'Project': result,
                        'Publication': result1,
                        'Honors_and_Award': result2,
                        'Patent': result3}), 200
    except Exception as e:
        return jsonify({'msg': "No data present " + str(e)}), 401

@app.route('/Verify/password',methods=['POST']  )
@token_required
def verifypassword(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)

        if jsondata['password']==''or jsondata is None or jsondata['password'] is None or not db.check(jsondata['password']):
            raise Exception
    except Exception as e:
        return jsonify({'msg': "No data present "+str(e)}), 401

    query1 = "SELECT [Password] FROM [dbo].[user_info] WHERE Euid = '" + data['user'] + "'"
    result = (db.query(query1, 0))
    if jsondata['password']==result[0]:
        return jsonify({'msg': 'password verified'}), 200

    return jsonify({'msg': "wrongpassword"}), 401




# type_check = ('Name','Email','Password','Phone_No','Qualifications','University',)
#
# @app.route('/update/<type>' ,methods=['POST'] )
# @token_required
# def update(data,type):
#     try:
#         jsondata = request.get_data().decode("utf-8")
#         jsondata = json.loads(jsondata)
#         if jsondata[type]==''or jsondata is None or jsondata[type] is None:
#             raise Exception
#         if type not in type_check:
#            raise Exception
#         if type=='' or type is None or type=="" or not db.check(type):
#             return Exception
#     except Exception as e:
#         return jsonify({'msg': "No data present " + str(e)}), 401
#     query  = "UPDATE [dbo].[user_info] SET "+type+ " = '"+jsondata[type]+"' WHERE Euid = '"+ data['user']  +"';"
#     result = (db.query(query, 2))
#     if(result == 'Finished'):
#         return jsonify({'msg': 'updated'}), 200
#     return jsonify({'msg': 'updated'}), 405
#
#


@app.route('/user/authorlist')
@token_required
def authorlist(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)

        if jsondata['paperid'] == '' or jsondata is None or jsondata['paperid'] is None or not db.check( jsondata['paperid']):
            raise Exception
        query =  "SELECT * FROM [dbo].[Paper_author] WHERE Paper_key ="+ jsondata['paperid']
        print(query)
        result = db.query(query,1)
        return jsonify({'Status': result}), 200

    except Exception as e:
        return jsonify({'msg': "No data present " + str(e)}), 401


# @app.route('/user/paper')
# @token_required
# def paper(data):
#     try:
#         jsondata = request.get_data().decode("utf-8")
#         jsondata = json.loads(jsondata)
#
#         if jsondata['paperid'] == '' or jsondata is None or jsondata['paperid'] is None or not db.check( jsondata['paperid']):
#             raise Exception
#         query =  "SELECT * FROM [dbo].[research_paper] WHERE paper_pkey ="+ jsondata['paperid']+" AND Euid ='"+data['user']+"'"
#         result = db.query(query,0)
#         return jsonify({'Status': result}), 200
#
#     except Exception as e:
#         return jsonify({'msg': "No data present " + str(e)}), 401
















# extra code
# def run_query(query1):d
#     try:
#
#         try:
#
#             cursor = connection.cursor()
#             cursor.execute(query1)
#             result = cursor.fetchall()
#             cursor.close()
#             return  result
#         except Exception as e:
#             return str(e)
#     except Exception as e:
#         return  str(e)


# def login_query(query1,query2):
#         try:
#
#             cursor = connection.cursor()
#             cursor.execute(query1)
#             result = cursor.fetchone()
#             cursor.execute(query2)
#             result1 =cursor.fetchone()
#             connection.commit()
#             cursor.close()
#             a = [result[0],result1[0],result1[1]]
#             return  a
#         except Exception as e:
#             connection.close()
#             return str(e)


#
# def register_query(query1,query2):
#
#         try:
#
#             cursor = connection.cursor()
#             cursor.execute(query1)
#             cursor.execute(query2)
#             connection.commit()
#             return jsonify({'msg': 'inserted', }), 200
#         except Exception as e:
#              return jsonify({'msg': str(e)}), 401
