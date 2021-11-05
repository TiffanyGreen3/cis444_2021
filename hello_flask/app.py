from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import datetime
import bcrypt
#import simplejson as json
from datetime import datetime
from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"
JWT_SECRET = None

global_db_con = get_db()


with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

#@app.route('/backp',  methods=['POST']) #endpoint
#def backp():
#    print(request.form)
#    salted = bcrypt.hashpw( bytes(request.form['fname'],  'utf-8' ) , bcrypt.gensalt(10))
#    print(salted)

#    print(  bcrypt.checkpw(  bytes(request.form['fname'],  'utf-8' )  , salted ))

#    return render_template('backatu.html',input_from_browser= str(request.form) )


@app.route('/auth',  methods=['POST']) #endpoint
def auth():
        print(request.form)
        return json_response(data=request.form)



#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    return render_template('server_time.html', server_time= str(datetime.datetime.now()) )

@app.route('/getTime') #endpoint
def get_time():
    return json_response(data={"password" : request.args.get('password'),
                                "class" : "cis44",
                                "serverTime":str(datetime.datetime.now())
                            }
                )

@app.route('/auth2') #endpoint
def auth2():
    jwt_str = jwt.encode({"username" : "cary",
                            "age" : "so young",
                            "books_ordered" : ['f', 'e'] } 
                            , JWT_SECRET, algorithm="HS256")
    #print(request.form['username'])
    return json_response(jwt=jwt_str)

@app.route('/exposejwt') #endpoint
def exposejwt():
    jwt_token = request.args.get('jwt')
    print(jwt_token)
    return json_response(output=jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))


@app.route('/hellodb') #endpoint
def hellodb():
    cur = global_db_con.cursor()
    cur.execute("insert into music values( 'dsjfkjdkf', 1);")
    global_db_con.commit()
    return json_response(status="good")

#Assigment 3

@app.route('/checkuser',  methods=['POST']) #endpoint
def checkuser():
    print(request.form)
    jwt_str = jwt.encode({"username" : request.form['fname'],"password" : request.form['lname'] }, JWT_SECRET, algorithm="HS256")
    #print(  bcrypt.checkpw(bytes(request.form['fname'],  'utf-8' )))
    return json_response(jwt=jwt_str)

#addUser
@app.route('/createPerson',  methods=['POST']) #endpoint
def createPerson ():
    print(request.form)
    newP = request.form['nameP']
    newPas = request.form['new_Pass']
    salted = bcrypt.hashpw( bytes(request.form['new_Pass'],  'utf-8' ) , bcrypt.gensalt(10))
    #print(newPas)
    print(salted)

    submit = "INSERT INTO users(username,password) VALUES('"
    submit += str (newP)
    submit += "','"
    submit += str (salted.decode('utf-8'))
    submit += "');"
    print(submit)

    cur = global_db_con.cursor()
    cur.execute(submit)
    global_db_con.commit()

    return json_response(status='good')

#authUser
@app.route('/userTest',  methods=['POST']) #endpoint
def userTest():
    print(request.form)
    #print("++++++++++++++++++++++ ")

    cur = global_db_con.cursor()
    pName = "select password from users where username ='"
    pName += request.form['nameUser']
    pName += "';"
    #print(pName)
    cur.execute(pName)
    r = cur.fetchone()
    #print(str(r[0]))
    user_Password = str(r[0])
    if bcrypt.checkpw(bytes(request.form['wordPass'],'utf-8'), user_Password.encode('utf-8')):
        jwt_str = jwt.encode({"username" : request.form['nameUser'],"password" : request.form['wordPass'] }, JWT_SECRET, algorithm="HS256")
       # print("++++++++++++++++++++++")
       # print(jwt_str)
        return json_response(jwt = jwt_str)
    print("Not Valid")
    return json_response(status='404', msg='Not Valid User')

#Getting the books
@app.route('/getBooks',  methods=['GET']) #endpoint
def getBooks():

    print("YAY Vaild")
    cur = global_db_con.cursor()
    books_Name_request = "SELECT book_name FROM books;"
    cur.execute(books_Name_request)
    books_Name_resp = cur.fetchall()
    print(books_Name_resp)

    books_Price_request = "SELECT book_price FROM books;"
    cur.execute(books_Price_request)
    books_Price_resp = cur.fetchall()
    print(books_Price_resp)
    return json_response(nameBooks = books_Name_resp, priceBook = books_Price_resp)

@app.route('/buyBook',  methods=['POST']) #endpoint
def buyBook():
    print ("you are buying")
    list_myBooks= request.form['books_names']
    print (list_myBooks)
    purch= datetime.now()
    dt_string = purch.strftime("%m/%d/%Y %H:%M:%S")
    print(dt_string)

    #cur = global_db_con.cursor()
    #update_buy = "update purchases set book_name = '"+list_myBooks+"%' where userName = John;"
    #cur.execute(update_buy)
    #list_myBooks= request.form['books']
    #global_db_con.commit()
    return render_template('first_form.html',dt_string)





#test run
#@app.route('/userTest',  methods=['POST']) #endpoint
#def userTest():
#    print(request.form)
   # print(  bcrypt.checkpw(  bytes(request.form['fname'],  'utf-8' )  , salted ))
 #   return render_template('backatu.html',input_from_browser= str(request.form) )


app.run(host='0.0.0.0', port=80)


