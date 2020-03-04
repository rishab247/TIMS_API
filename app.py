import pypyodbc
from flask import Flask, jsonify, request, make_response, logging
import jwt
import json
import datetime
import database as db
from functools import wraps

app = Flask(__name__)

app.config[
    'SECRET_KEY'] = 'super_safe_67uy67uy54tre3we098uy6t5r1q2we345ty7u8io90secretasas33323232as23as2a3s2s3a2s3a2s32a3s'


# # connection
# try:
#     connection = db.getconnection()
# except:
#     try:
#         connection = db.getconnection()
#     except Exception as e:
#         print(str(e))


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
    query = "SELECT  [Status] ,[HOD] FROM [dbo].[Status]where Euid = ? "
    result = db.query(query, 0, [data['user']])
    return jsonify({'Status': result[0],
                    'Hod': result[1]}), 200


@app.route('/login')
def login():
    try:
        auth = request.authorization
        if auth is None:
            return make_response({'msg': 'Login req'}, 401, {'msg': 'Login req'})
        if auth.username == '' or auth.password == '':
            return make_response({'msg': 'Login req'}, 401, {'msg': 'Login req'})
        if not db.check(auth.username) or not db.check(auth.password):
            return make_response({'msg': 'Login req'}, 401, {'msg': 'Login req'})
        query1 = 'SELECT [Password] FROM [dbo].[user_info] WHERE Euid = ?'
        query2 = 'SELECT  [HOD],[Hod_Department] FROM [dbo].[Status]where Euid = ? '
        result = (db.query(query1, 0, [auth.username]))
        result1 = (db.query(query2, 0, [auth.username]))
        query = "SELECT  [Status] FROM [dbo].[Status]where Euid = ? "
        result3 = db.query(query, 0, [auth.username])
        print((result3[0]))
        if result is None:
            return jsonify({'msg': 'incorrect username'}), 401
        if auth and auth.password == result[0]:
            token = jwt.encode({'user': auth.username, 'HOD':  (result1[0]),
                                'hod_department': (result1[1]),
                                'Verify':result3[0],
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                               app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('UTF-8')})
        return make_response({'msg': 'Login req'}, 401, {'msg': 'Login req'})
    except Exception as e:
        print(str(e))
        return jsonify({"msg": 'error1'}), 401


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_data().decode("utf-8")
        data = json.loads(data)
        if not db.check(data['Euid']) or not db.check(data['Name']) or not db.Email_check(
                data['Email']) or not db.check(data['Password']) or \
                not db.check(data['Phone_No']) or not db.check(data['Department_Name']) or not db.check(data['DOJ']) or \
                not db.check(data['Qualifications']) or not db.check(data['University']) or not db.check(data['DOB']) or \
                not db.check(data['Hod_Department']):
            raise Exception("format")
        if (db.query(
                "SELECT CASE WHEN EXISTS (select * from user_info where Euid= ? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
                0, [str(data['Euid'])])[0]):
            return jsonify({'msg': "Dublicate Euid "}), 401
        if (db.query(
                "SELECT CASE WHEN EXISTS (select * from user_info where Email= ? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",0,
                [(data['Email'])])[0]):
            return jsonify({'msg': "Dublicate Email "}), 401
        # query1 = "INSERT INTO [dbo].[user_info] VALUES ("
        # query1 = query1 + "'" + data['Euid'] + "',"
        # query1 = query1 + "'" + data['Name'] + "',"
        # query1 = query1 + "'" + data['Email'] + "',"
        # query1 = query1 + "'" + data['Password'] + "',"
        # query1 = query1 + "'" + data['Phone_No'] + "',"
        # query1 = query1 + "'" + data['Department_Name'] + "',"
        # query1 = query1 + "'" + data['DOJ'] + "',"
        # query1 = query1 + "'" + data['Qualifications'] + "',"
        # query1 = query1 + "'" + data['University'] + "',"
        # query1 = query1 + "'" + data['DOB'] + "'" + ");"
        # query2 = "INSERT INTO [dbo].[Status] VALUES ("
        # query2 = query2 + "'" + data['Euid'] + "',"
        # query2 = query2 + "0,"+ data['type']+","
        # query2 = query2 + "'" + data['Name'] + "',"
        # query2 = query2 + "'" + data['Hod_Department'] + "');"
        result1 = (db.query("INSERT INTO [dbo].[user_info] VALUES (?,?,?,?,?,?,?,?,?,?);", 2,
                            [data['Euid'], data['Name'], data['Email'], data['Password'], data['Phone_No'],
                             data['Department_Name'], data['DOJ'], data['Qualifications'], data['University'],
                             data['DOB']]))
        if data['type'] =='1':
            result3 = (db.query("INSERT INTO [dbo].[Faculty_info] VALUES (?,?,?,?,?,?,?,?,?);", 2,
                            [data['Euid'], data['Name'], data['Phone_No'],data['Email'],
                             data['Department_Name'], data['DOJ'],data['DOB'], data['Qualifications'], data['University']]))
        else:
            result3='Finished'
        result2 = (db.query("INSERT INTO [dbo].[Status] VALUES (?,?,?,?,?);", 2,
                            [data['Euid'], 0, data['type'], data['Name'], data['Hod_Department']]))

        if result1 == 'Finished' and result2 == 'Finished'and result3 == 'Finished':
            return jsonify({'msg': 'inserted', }), 200
        return jsonify({'msg': result1 + '   ' + result2, }), 401
    except Exception as e:
        return jsonify({"msg": 'error'}), 401


@app.route('/user/Profile', methods=['GET'])
@token_required
def userdata(data):
    query = "SELECT [Euid],[Name],[Email],[Phone_No],[Department_Name],[DOJ],[Qualifications],[University],[DOB] FROM [dbo].[user_info]where Euid = ? "
    result = db.query(query, 0, [data['user']])
    print(result)
    a = "noimage"
    result1 = a.split(" ")
    print(result1)
    if (db.query(
            "SELECT CASE WHEN EXISTS (select * from [Profile_image] where Euid= ? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
            0, [data['user']])[0]):
        query = "select Image from [Profile_image] where Euid = ?"
        result1 = db.query(query, 1, [data['user']])
        result1 = str(result1[0])[13:-4]
        result1 = result1.strip().split(" ")
    return jsonify({'Status': result, 'pic': result1}), 200


@app.route('/user/Accomplishment')
@token_required
def useraccomplishment(data):
    # query = "SELECT  * FROM [dbo].[research_paper] where Euid = '" + data['user'] + "' "
    try:
        try:
            result = db.query("SELECT  Pid,Title,Date FROM [dbo].[Project_1] where Euid = ? ", 1, [data['user']])
        except Exception as e:
            result = "No data present" + 'error'
        try:
            result1 = db.query("SELECT  Pu_id,Title,Date FROM [dbo].[Publication] where Euid = ? ", 1, [data['user']])
        except Exception as e:
            result1 = "No data present" + 'error'
        try:
            result2 = db.query("SELECT  PKEY,Title,Date FROM [dbo].[Honors_and_Award] where Euid = ? ", 1,
                               [data['user']])
        except Exception as e:
            result2 = "No data present" + 'error'
        try:
            result3 = db.query("SELECT  Pa_id,Title,Date FROM [dbo].[Patent] where Euid = ? ", 1, [data['user']])
        except Exception as e:
            result3 = "No data present" + 'error'
        return jsonify({'Project': result,
                        'Publication': result1,
                        'Honors_and_Award': result2,
                        'Patent': result3}), 200
    except Exception as e:
        return jsonify({'msg': "No data present " + 'error'}), 401


@app.route('/user/Accomplishmen/Details', methods=['POST'])
@token_required
def useraccomplishmendetails(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)
        # 'id','Type',''
        if not db.check(jsondata['Type']) or not db.check(jsondata['id']) or jsondata['Type'] == '' or jsondata[
            'id'] == '' or jsondata['Type'] is None or jsondata['id'] is None:
            return jsonify({'msg': 'error2'}), 401

        if jsondata['Type'] == 'Publication':
            try:
                result = db.query("SELECT  * FROM [dbo].[Publication] where Pu_id = ? ", 0, [jsondata['id']])
                result1 = db.query(
                    " select * from author where aid in ( select aid from publication_author where Pu_id = ?)", 1,
                    [jsondata['id']])

                if result1 == None or result == None or result1 == 'None' or result == 'None':
                    raise Exception
                if not verifypassword(data, jsondata['id'], jsondata['Type']):
                    raise Exception
            except Exception as e:
                return jsonify({'msg': 'error1' + str(e)}), 401
            return jsonify({'data': result, 'author': result1}), 200

        elif jsondata['Type'] == 'Project':
            try:
                result = db.query("SELECT  * FROM [dbo].[Project_1] where Pid = ? ", 0, [jsondata['id']])
                result1 = db.query(" select * from author where aid in ( select aid from project_author where Pid = ?)",
                                   1, [jsondata['id']])
                if result1 == None or result == None or result1 == 'None' or result == 'None':
                    raise Exception
                if not verifypassword(data, jsondata['id'], jsondata['Type']):
                    raise Exception
            except Exception as e:
                return jsonify({'msg': 'error'}), 401
            return jsonify({'data': result, 'author': result1}), 200


        elif jsondata['Type'] == 'Patent':
            try:
                result = db.query("SELECT  * FROM [dbo].[Patent] where Pa_id = ? ", 0, [jsondata['id']])
                result1 = db.query(
                    " select * from author where aid in ( select aid from patent_author where Pa_id = ?)", 1,
                    [jsondata['id']])

                if result1 == None or result == None or result1 == 'None' or result == 'None':
                    raise Exception
                if not verifypassword(data, jsondata['id'], jsondata['Type']):
                    raise Exception
            except Exception as e:
                return jsonify({'msg': 'error'}), 404
            return jsonify({'data': result, 'author': result1}), 200
        elif jsondata['Type'] == 'HonorsandAward':
            try:
                result = db.query("SELECT  * FROM [dbo].[Honors_and_Award] where PKEY = ? ", 0, [jsondata['id']])
                if result == None or result == 'None':
                    raise Exception
                if not verifypassword(data, jsondata['id'], jsondata['Type']):
                    raise Exception
            except Exception as e:
                return jsonify({'msg': 'error'}), 404
            return jsonify({'data': result}), 200
        else:
            return jsonify({'msg': 'Type error'+jsondata['Type']}), 401


    except Exception as e:
      return jsonify({'msg': 'error3'+str(e)}), 401


@app.route('/author/list')
@token_required
def authorlist(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)

        if jsondata['paperid'] == '' or jsondata is None or jsondata['paperid'] is None or not db.check(
                jsondata['paperid']):
            raise Exception
        query = "SELECT * FROM [dbo].[Paper_author] WHERE Paper_key = ?"
        result = db.query(query, 1, [jsondata['paperid']])
        return jsonify({'Status': result}), 200

    except Exception as e:
        return jsonify({'msg': "No data present " + 'error'}), 401


@app.route('/author/search', methods=['POST'])
@token_required
def authorsearch(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)

        if jsondata['author_Email'] == '' or jsondata is None or jsondata['author_Email'] is None or not db.Email_check(
                jsondata['author_Email']):
            raise Exception
        query1 = "SELECT [Aid] FROM [dbo].[Author] WHERE Email = ?"
        result = (db.query(query1, 0, [jsondata['author_Email']]))
        return jsonify({'msg': result[0]}), 200
    except Exception as e:
        return jsonify({'msg': "No data present " + 'error'}), 401


@app.route('/user/upload/Publication', methods=['POST'])
@token_required
def Accomplishmentuploadpublication(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)
        # 'noofauthor'  'Type'  'author'
        if not db.check(jsondata['noofauthor']) or not db.check(jsondata['Title']) or not db.check(jsondata['type']) \
                or not db.check(jsondata['Date']) or not db.check(jsondata['Description']) or not db.check(jsondata['Publication_or_publisher']) \
                or jsondata['noofauthor'] == '' or jsondata['Title'] == '' or jsondata['Publication_or_publisher'] == '' or jsondata['type'] == '' \
                or jsondata['Date'] == '' or jsondata['Description'] == '' or jsondata['noofauthor'] is None or jsondata['type'] is None or \
                jsondata['Title'] is None or jsondata['Publication_or_publisher'] is None or jsondata['Date'] is None or jsondata['Description'] is None:
            raise Exception
        if (db.query(
                " SELECT CASE WHEN EXISTS (select * from Publication where Euid= ? and title= ? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
                0, [data['user'], jsondata['Title']])[0]):
            return jsonify({'msg': "Dublicate entry "}), 401
        query1 = "insert into Publication values(?,?,?,?,?,?,?) "
        result = (db.query(query1, 2, [jsondata['Title'], jsondata['Publication_or_publisher'], jsondata['Date'],
                                       jsondata['Description'], jsondata['url'], data['user'],jsondata['type']]))
        print(result+"123")
        if result is not 'Finished':
            raise Exception
        result = str(db.query1(" select  @@IDENTITY", 1))

        result = result[11:-5]

        result = int(result)
        author_list_id = list(jsondata['author'])
        noofauthor = int(jsondata['noofauthor'])
        author_type_list = jsondata['typeofauthor']
        no_new_author = author_type_list.count(1)
        no_old_author = author_type_list.count(0)
        new_author_data = (jsondata['authordata'])

        print(str(noofauthor) + "   " + str(no_old_author) + "   " + str(no_new_author))
        if int(no_new_author + no_old_author) != int(noofauthor):
            raise Exception
        if len(author_list_id) != int(no_old_author):
            raise Exception
        for i in range(no_new_author):
            print(i)
            author_list_id.append(int(addauthor(new_author_data[i])))

        print(author_list_id)
        for i in range(0, int(jsondata['noofauthor'])):
            print(author_list_id[i])
            query1 = "insert into publication_author values(?, ?)"
            result1 = (db.query(query1, 2, [str(author_list_id[i]), str(result)]))
            if result1 is not 'Finished':
                raise Exception
        print(author_list_id)
        return jsonify({'msg': author_list_id}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'msg': "No data present " + 'error'}), 401


@app.route('/user/upload/Project', methods=['POST'])
@token_required
def Accomplishmentuploadproject(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)
        # 'noofauthor'  'Type'  'author'
        if not db.check(jsondata['noofauthor']) or not db.check(jsondata['Title']) \
                or not db.check(jsondata['Date']) or not db.check(jsondata['Description']) \
                or jsondata['noofauthor'] == '' or jsondata['Title'] == '' \
                or jsondata['Date'] == '' or jsondata['Description'] == '' or jsondata['noofauthor'] is None or \
                jsondata['Title'] is None \
                or jsondata['Date'] is None or jsondata['Description'] is None:
            raise Exception("22")
        if (db.query(
                " SELECT CASE WHEN EXISTS (select * from Project_1 where Euid= ? and title=? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
                0, [data['user'], jsondata['Title']])[0]):
            return jsonify({'msg': "Dublicate entry "}), 401
        query1 = "insert into Project_1 values(?,?,?,?,?); "
        result = (db.query(query1, 2,[jsondata['Title'], jsondata['Date'], jsondata['Description'], jsondata['url'], data['user']]))
        print(result)
        if result is not 'Finished':
            raise Exception
        result = str(db.query("select @@IDENTITY", 1,[]))
        result = result[11:-5]
        result = int(result)
        author_list_id = list(jsondata['author'])
        noofauthor = int(jsondata['noofauthor'])
        author_type_list = jsondata['typeofauthor']
        no_new_author = author_type_list.count(1)
        no_old_author = author_type_list.count(0)
        new_author_data = (jsondata['authordata'])

        print(str(noofauthor) + "   " + str(no_old_author) + "   " + str(no_new_author))
        if int(no_new_author + no_old_author) != int(noofauthor):
            raise Exception
        if len(author_list_id) != int(no_old_author):
            raise Exception
        for i in range(no_new_author):
            print(i)
            author_list_id.append(int(addauthor(new_author_data[i])))

        print(author_list_id)
        for i in range(0, int(jsondata['noofauthor'])):
            print(author_list_id[i])
            query1 = "insert into project_author values(?,?)"
            result1 = (db.query(query1, 2, [str(author_list_id[i]), str(result)]))
            if result1 is not 'Finished':
                raise Exception
        print(author_list_id)
        return jsonify({'msg': author_list_id}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'msg': "No data present " + 'error'}), 401


@app.route('/user/upload/Honors_and_Award', methods=['POST'])
@token_required
def Accomplishmentuploadhonor(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)
        if not db.check(jsondata['Title']) or not db.check(jsondata['Issuer']) \
                or not db.check(jsondata['Date']) or not db.check(jsondata['Description']) \
                or jsondata['Title'] == '' or jsondata['Issuer'] == '' \
                or jsondata['Date'] == '' or jsondata['Description'] == '' or \
                jsondata['Title'] is None or jsondata['Issuer'] is None \
                or jsondata['Date'] is None or jsondata['Description'] is None:
            raise Exception
        if (db.query(
                " SELECT CASE WHEN EXISTS (select * from Honors_and_Award where Euid= ? and title=? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
                0, [data['user'], jsondata['Title']])[0]):
            return jsonify({'msg': "Dublicate entry "}), 401
        query1 = "insert into Honors_and_Award values(?,?,?,?,? ) "
        result = (db.query(query1, 2, [data['user'], jsondata['Title'], jsondata['Issuer'], jsondata['Date'],
                                       jsondata['Description']]))
        if result is not 'Finished':
            raise Exception
        print(result)
        return jsonify({'msg': "inserted"}), 200
    except Exception as e:
        return jsonify({'msg': "No data present " + 'error'}), 401


@app.route('/user/upload/Patent', methods=['POST'])
@token_required
def Accomplishmentuploadpatent(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)
        # 'noofauthor'  'Type'  'author'
        if not db.check(jsondata['noofauthor']) or not db.check(jsondata['Title']) \
                or not db.check(jsondata['Date']) or not db.check(jsondata['Description']) or not db.check(
            jsondata['Patent_office']) \
                or not db.check(jsondata['Application_no']) or jsondata['noofauthor'] == '' or jsondata['Title'] == '' \
                or jsondata['Date'] == '' or jsondata['Description'] == '' or jsondata['Patent_office'] == '' or \
                jsondata['Application_no'] == '' or jsondata['noofauthor'] is None or \
                jsondata['Title'] is None or jsondata['Patent_office'] is None or jsondata['Application_no'] is None \
                or jsondata['Date'] is None or jsondata['Description'] is None:
            raise Exception("22")
        if (db.query(
                " SELECT CASE WHEN EXISTS (select * from [Patent] where Euid=? and Application_no=?) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
                0, [data['user'], jsondata['Application_no']])[0]):
            return jsonify({'msg': "Dublicate entry "}), 401
        query1 = "insert into [Patent] values(?,?,?,?,?,?,?) "
        result = (db.query(query1, 2,
                           [jsondata['Title'], jsondata['Patent_office'], jsondata['Application_no'], jsondata['Date'],
                            jsondata['Description'], jsondata['url'], data['user']]))
        print(query1)
        if result is not 'Finished':
            raise Exception
        result = str(db.query(" select  @@IDENTITY;", 1,[]))
        result = result[11:-5]
        result = int(result)
        author_list_id = list(jsondata['author'])
        noofauthor = int(jsondata['noofauthor'])
        author_type_list = jsondata['typeofauthor']
        no_new_author = author_type_list.count(1)
        no_old_author = author_type_list.count(0)
        new_author_data = (jsondata['authordata'])

        print(str(noofauthor) + "   " + str(no_old_author) + "   " + str(no_new_author))
        if int(no_new_author + no_old_author) != int(noofauthor):
            raise Exception
        if len(author_list_id) != int(no_old_author):
            raise Exception
        for i in range(no_new_author):
            print(i)
            author_list_id.append(int(addauthor(new_author_data[i])))

        print(author_list_id)
        for i in range(0, int(jsondata['noofauthor'])):
            print(author_list_id[i])
            query1 = "insert into [patent_author] values(?,?)"
            print(query1)
            result1 = (db.query(query1, 2, [str(author_list_id[i]), str(result)]))
            if result1 is not 'Finished':
                raise Exception
        print(author_list_id)
        return jsonify({'msg': author_list_id}), 200
    except Exception as e:
        return jsonify({'msg': "No data present " + 'error'}), 401


@app.route('/user/upload', methods=['DELETE'])
@token_required
def Accomplishmentdelete(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)
        #   'Type'  'id' 'author_id'

        if not db.check(jsondata['Type']) or not db.check(jsondata['password']) \
                or not db.check(jsondata['id']) or jsondata['Type'] == '' or jsondata['id'] == '' or jsondata[
            'password'] == '' or \
                jsondata['Type'] is None or jsondata['id'] is None or jsondata['password'] is None:
            raise Exception("   1   ")
        if not verifypassword10(data, jsondata):
            return jsonify({'msg': "incorrect password"}), 401
        if jsondata["Type"] == 'Project':
            query = "SELECT CASE WHEN EXISTS (select * from [Project_1] where Euid=? and Pid= ? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END"
            list = [data['user'], jsondata['id']]
            query1 = "SELECT CASE WHEN EXISTS (select * from [project_author] where Pid= ? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END"
            list1 = [jsondata['id']]
            delquery = " DELETE from [Project_1] where Euid= ? and Pid= ?"
            dellist = [data['user'], jsondata['id']]
            delquery1 = " DELETE from [project_author] where Pid= ?"
            dellist1 = [jsondata['id']]
        elif jsondata["Type"] == 'Publication':
            query = "SELECT CASE WHEN EXISTS (select * from [Publication] where Euid= ? and pu_id=? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END"
            list = [data['user'], jsondata['id']]
            query1 = "SELECT CASE WHEN EXISTS (select * from [publication_author] where  pu_id=? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END"
            list1 = [jsondata['id']]
            delquery = " DELETE from [publication ] where Euid=? and pu_id=?"
            dellist = [data['user'], jsondata['id']]
            delquery1 = " DELETE from [publication_author] where pu_id= ?"
            dellist1 = [jsondata['id']]
        elif jsondata["Type"] == "Patent":
            query = "SELECT CASE WHEN EXISTS (select * from [Patent] where Euid=? and pa_id= ? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END"
            list = [data['user'], jsondata['id']]
            query1 = "SELECT CASE WHEN EXISTS (select * from [patent_author] where pa_id=?) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END"
            list1 = [jsondata['id']]
            delquery = " DELETE from [Patent] where Euid= ? and pa_id=?"
            dellist = [data['user'], jsondata['id']]
            delquery1 = " DELETE from [patent_author] where pa_id=?"
            dellist1 = [jsondata['id']]
        elif jsondata["Type"] == "HonorsandAward":
            query = "SELECT CASE WHEN EXISTS (select * from [Honors_and_Award] where Euid= ? and PKEY= ? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END"
            list = [data['user'], jsondata['id']]
            query1 = ''
            list1 = []
            delquery = " DELETE from [Honors_and_Award] where Euid= ? and PKEY = ? "
            dellist = [data['user'], jsondata['id']]
            delquery1 = ''
            dellist1 = []

        else:
            return jsonify({'msg': "Wrong type"}), 401

        if not db.query(query, 0, list)[0]:
            return jsonify({'msg': "Does not exist "}), 401
        if query1 != '':
            if not db.query(query1, 0, list1)[0]:
                return jsonify({'msg': "Author not exist "}), 401

        if delquery1 != "":
            result = db.query(delquery1, 2, dellist1)
            print("delquery1" + str(result ))
            if  str(result) != "Finished":
                raise Exception

        result1 = db.query(delquery, 2, dellist)
        print("delquery" +str(result1))
        if str(result1) != "Finished":
            raise Exception
        return jsonify({'msg': "Deleted"}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'msg': "No data present " + 'error'}), 401


@app.route('/user/Profile', methods=['PUT'])
@token_required
def updateuserdata(data):
    try:
        if not (db.query(
                " SELECT CASE WHEN EXISTS (select * from [user_info] where Euid= ? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
                0, [data['user']])[0]):
            return jsonify({'msg': "User doen't exist"}), 401
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)
        if not db.check(jsondata['password']) or not db.check(jsondata['Department_Name']) \
                or not db.check(jsondata['phoneno']) or not db.check(jsondata['Qualification']) or not db.check(
            jsondata['University']) or \
                jsondata['Department_Name'] == '' or jsondata['Qualification'] == '' or jsondata['University'] == '' or \
                jsondata['pic'] == '' or jsondata['phoneno'] == '' or \
                jsondata['Department_Name'] is None or jsondata['pic'] is None or jsondata['Qualification'] is None or \
                jsondata['University'] is None or jsondata['phoneno'] is None:
            return jsonify({'msg': "Not Allowed"}), 405

        if not verifypassword10(data, jsondata):
            return jsonify({'msg': "Wrong Password  22"}), 401
        query = "UPDATE [dbo].[user_info] SET [Phone_No] = ?,[Department_Name] = ?,[Qualifications] = ?,[University] = ? WHERE [Euid] =	? "
        result = db.query(query, 2, [jsondata['phoneno'], jsondata["Department_Name"], jsondata["Qualification"],
                                     jsondata['University'], data['user']])
        result1 = 'Finished'
        if jsondata['pic'] != 'noimage' and result == 'Finished':
            if (db.query(
                    "SELECT CASE WHEN EXISTS (select * from [Profile_image] where Euid=?) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
                    0, [data['user']])[0]):
                query = "UPDATE [dbo].[Profile_image] SET [Image] = '"+jsondata['pic']+"' WHERE Euid = ?"
                list = [ data['user']]
            else:
                query = "INSERT INTO [dbo].[Profile_image] VALUES(?,'"+jsondata['pic']+"')"
                list = [data['user']]
            result1 = db.query(query, 2, list)
            print(result1)
        print(result)

        return jsonify({'msg': result, 'msg1': result1}), 200
    except Exception:
        return jsonify({'msg': "Error " + 'error'}), 401


@app.route('/Verify/password', methods=['PUT'])
@token_required
def verifypassword1(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)
        if not db.check(jsondata['password']) or not db.check(jsondata['new_password']) or \
                jsondata['password'] == '' or jsondata['new_password'] == '' or \
                jsondata['password'] is None or jsondata['new_password'] is None:
            return jsonify({'msg': "Not Allowed"}), 405
        if not (db.query(
                " SELECT CASE WHEN EXISTS (select * from [user_info] where Euid= ? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
                0, [data['user']])[0]):
            return jsonify({'msg': "User doen't exist"}), 401
        if not verifypassword10(data, jsondata):
            return jsonify({'msg': "Wrong Password  1"}), 401
        query = "UPDATE [dbo].[user_info] SET  [Password] =  '"+jsondata["new_password"]+"' WHERE [Euid] = ?  "
        result = db.query(query, 2, [  data['user']])
        print('password result'+str(result))
        return jsonify({'msg': result}), 200
    except Exception as e:
        return jsonify({'msg': "Error " + str(e)}), 401


@app.route('/report/download', methods=['POST'])
@token_required
def download(data):
    # dateend   datestart type
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)
        int(jsondata['dateend'])
        int(jsondata['datestart'])

        if not db.check(jsondata['dateend']) or not db.check(jsondata['type']) or not db.check(jsondata['datestart']) or \
                jsondata['dateend'] == '' or jsondata['datestart'] == '' or jsondata['type'] == '' or \
                jsondata['dateend'] is None or jsondata['datestart'] is None or jsondata['type'] is None:
            return jsonify({'msg': "Not Allowed"}), 405
        if jsondata['type'] == 'all':
            query = "select patent.Pa_id,title,Patent_office,Application_no,Date,Description,patent.URL ,Name,Email,Phoneno from patent, patent_author, author where author.aid in (select Aid from patent_author where Pa_id in(select Pa_id from patent where Euid=" + \
                    "?)) and author.aid=patent_author.Aid and patent.pa_id in(select Pa_id from patent where Euid=?)  and patent.pa_id=patent_author.pa_id and date BETWEEN ?  and ?"
            list = [data['user'],data['user'], jsondata['datestart'], jsondata['dateend']]
            query1 = "select project_author.Pid,Title,Date,Description,URL,Name,Email,Phoneno from Project_1, project_author, author where author.aid in (select Aid from project_author where Pid in(select Pid from Project_1 where Euid=" + \
                     "?)) and author.aid=project_author.Aid and Project_1.Pid=project_author.Pid and  Project_1.Pid in (select Pid from Project_1 where Euid=?) and date BETWEEN ? and ?"
            query2 = "select Publication.Pu_id ,Title, Publication_or_publisher,Date,Type,Description,URL,name , Email,Phoneno from Publication, publication_author, author where author.aid in (select Aid from publication_author where Pu_id in(select Pu_id from Publication where Euid=" + \
                     "?)) and author.aid=publication_author.Aid and Publication.Pu_id=publication_author.Pu_id and Publication.Pu_id in (select Pu_id from Publication where Euid=?)  and Date BETWEEN ?  and ?"
            query3 = "select * from Honors_and_Award where Euid = ? and  Date BETWEEN ? and ?"
            list1 = [data['user'], jsondata['datestart'], jsondata['dateend']]

            result = db.query(query, 1, list)
            result1 = db.query(query1, 1, list)
            result2 = db.query(query2, 1, list)
            result3 = db.query(query3, 1, list1)
            return jsonify({'Patent': result,
                            'Project': result1,
                            'Publication': result2,
                            'Honors_and_Award': result3}), 200
        elif jsondata['type'] == 'Patent':
            query = "select patent.Pa_id,title,Patent_office,Application_no,Date,Description,patent.URL ,Name,Email,Phoneno from patent, patent_author, author where author.aid in (select Aid from patent_author where Pa_id in(select Pa_id from patent where Euid=" + \
                    "?)) and author.aid=patent_author.Aid and patent.pa_id=patent_author.pa_id and patent.pa_id in(select Pa_id from patent where Euid=?)  and date BETWEEN ?  and ?"
            list = [data['user'],data['user'], jsondata['datestart'], jsondata['dateend']]

            result = db.query(query, 1, list)
            return jsonify({'Patent': result}), 200
        elif jsondata['type'] == 'Publication':
            query2 = "select Publication.Pu_id ,Title, Publication_or_publisher,Date,Type,Description,URL,name , Email,Phoneno from Publication, publication_author, author where author.aid in (select Aid from publication_author where Pu_id in(select Pu_id from Publication where Euid=" + \
                     "?))and author.aid=publication_author.Aid and Publication.Pu_id=publication_author.Pu_id and Publication.Pu_id in (select Pu_id from Publication where Euid=?)  and Date BETWEEN ? and ?"
            list = [data['user'],data['user'], jsondata['datestart'], jsondata['dateend']]

            result1 = db.query(query2, 1, list)
            return jsonify({'Publication': result1}), 200
        elif jsondata['type'] == 'Project':
            query1 = "select project_author.Pid,Title,Date,Description,URL,Name,Email,Phoneno from Project_1, project_author, author where author.aid in (select Aid from project_author where Pid in(select Pid from Project_1 where Euid=" + \
                     "?)) and author.aid=project_author.Aid and Project_1.Pid=project_author.Pid and  Project_1.Pid in (select Pid from Project_1 where Euid=?) and date BETWEEN ?  and ?"
            list = [data['user'], data['user'], jsondata['datestart'], jsondata['dateend']]

            result1 = db.query(query1, 1, list)
            return jsonify({
                'Project': result1}), 200
        elif jsondata['type'] == 'HonorsandAward':
            query3 = "select * from Honors_and_Award where Euid = ? and  Date BETWEEN ?  and ?"
            list = [data['user'], jsondata['datestart'], jsondata['dateend']]

            result1 = db.query(query3, 1, list)
            return jsonify({
                'Honors_and_Award': result1}), 200
        else:
            raise Exception




    except:
        return jsonify({'msg': "Error "}), 401


@app.route('/facultylist', methods=['POST'])
@token_required
def facultylist(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)
        if data['HOD']==True and data['Verify']==True:
            if not db.check(jsondata['Department']) or \
                    jsondata['Department'] == '' or \
                    jsondata['Department'] is None:
                return jsonify({'msg': "Not Allowed"}), 405
            if (jsondata['Department'] == 'all'):
                query = "select faculty_info.*, Status.Status from faculty_info,Status where Status.Euid =Faculty_info.Euid"
                list1 = []

            else:
                query = "select faculty_info.*, Status.Status from faculty_info,Status where Status.Euid =Faculty_info.Euid and Faculty_info.Department= ? "
                list1 = [jsondata['Department']]

            resutl = db.query(query, 1, list1)
            print(data['Verify'])
            print(data['HOD'])
            return jsonify({'msg': resutl}), 200
            # if(data)

        else:
            return jsonify({'msg': "Not Allowed"}), 405


    except:
        return jsonify({'msg': "Error "}), 401



@app.route('/facultyverify', methods=['POST'])
@token_required
def facultyverify(data):
    try:
        jsondata = request.get_data().decode("utf-8")
        jsondata = json.loads(jsondata)
        if data['HOD']==True and data['Verify']==True:
            if  jsondata['Euid'] == '' or len(jsondata['Euid'])==0 or\
                    jsondata['Euid'] is None  or type([]) != type (jsondata['Euid']) :
                return jsonify({'msg': "Not Allowed"}), 405
            test=0
            for i in jsondata['Euid'] :
                if not db.check(i)  :
                    test=1
                    break
            if test==1 :
                return jsonify({'msg': "Not Allowed"}), 405
            str =''
            for i in range(len(jsondata['Euid'])-1):
                str+='?,'
            str+='?'
            query = " update Status set Status.Status=1 from	Status where Euid in("+str+")"
            result  = db.query(query,2,jsondata['Euid'])
            print(result)
            if result!='Finished':
                raise ('not finished')
            return jsonify({'msg':result}), 200

            # if(data)

        else:
            return jsonify({'msg': "Not Allowed"}), 405


    except  Exception as e:
        print(e)
        return jsonify({'msg': "Error "}), 401











def addauthor(list):
    try:
        result = authorsearch1(list)
        print(result)
        if result is None:
            result = (db.query("insert into author values(?,?,?)", 2,[list[0] , list[1] , list[2]  ]))
            if result is not 'Finished':
                raise Exception

            result1 = (db.query("select @@IDENTITY", 0, []))
            # result1 = int(result1[11:-5])
            print(result)
            print(result1)
            return result1[0]
        return result
    except Exception as e:
        print(str(e))
        return "ddfsd" + 'error'


def authorsearch1(list):
    try:

        if list[1] == '' or list is None or list[1] is None or not db.Email_check(list[1]):
            raise Exception
        query1 = "SELECT [Aid] FROM [dbo].[Author] WHERE Email =  ?"
        result = (db.query(query1, 0, [list[1]]))
        if result is None or result == '':
            return None
        result = result[0]
        print(result)

        return result
    except Exception as e:
        return 'error'


def verifypassword(data, id, type):
    if type == 'Publication':
        try:
            result = db.query(
                "  SELECT CASE WHEN EXISTS (SELECT * from Publication where Euid = ? and pu_id = ?) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
                0, [data['user'], id])

            print(result)

            if result[0]:
                return True
            else:
                return False
        except Exception as e:
            return False


    elif type == 'Project':
        try:
            result = db.query(
                "SELECT CASE WHEN EXISTS (SELECT * from Project_1 where Euid = ? and pid = ?) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
                0, [data['user'], id])
            print(result)
            if result[0]:
                return True
            else:
                return False

        except Exception as e:
            return False


    elif type == 'Patent':
        try:
            result = db.query(
                "  SELECT CASE WHEN EXISTS (SELECT * from Patent where Euid = ? and pa_id = ?) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END",
                0, [data['user'], id])
            print(result)
            if result[0]:
                return True
            else:
                return False

        except Exception as e:
            return False
    elif type == 'HonorsandAward':
        try:
            result = db.query(
                "SELECT CASE WHEN EXISTS (select * from Honors_and_Award where Euid= ? and PKEY= ? ) THEN CAST (1 AS BIT) ELSE CAST (0 AS BIT) END ",
                0, [data['user'], id])
            print(result)
            if result[0]:
                return True
            else:
                return False

        except Exception as e:
            return False
    else:
        return False


def verifypassword10(data, jsondata):
    try:

        if jsondata['password'] == '' or jsondata is None or jsondata['password'] is None or not db.check(
                jsondata['password']):
            raise Exception

        query1 = "SELECT [Password] FROM [dbo].[user_info] WHERE Euid = ?"
        result = (db.query(query1, 0,[data['user']]))
        if jsondata['password'] == result[0]:
            return True

        return False
    except Exception as e:
        print( "verifypassword10"+ str(e))
        return False

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
#             return 'error'
#     except Exception as e:
#         return  'error'


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
