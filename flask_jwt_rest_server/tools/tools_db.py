#hjfn
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger
import bcrypt
from db_con import get_db_instance, get_db

global_db_con = get_db()

def check_password(password,username):

    cur = global_db_con.cursor()
    if check_person(username) == False:
        return False
    pName = "SELECT password FROM users WHERE username ='"
    pName += request.form['firstname']
    pName += "';"
    print(pName)
    cur.execute(pName)
    r = cur.fetchone()
    user_Password = str(r[0])
    if bcrypt.checkpw(bytes(request.form['password'],'utf-8'), user_Password.encode('utf-8')):
        return True
    return False

def check_person(username):
    cur = global_db_con.cursor()
    user_db = "SELECT EXISTS (SELECT username FROM users WHERE username = '"
    user_db += username
    user_db += "' limit 1)"
    print(user_db)
    cur.execute(user_db)
    r = cur.fetchone()
    print(r[0])
    if r[0] == True:
        return True
    return False

def createPerson ():
    print(request.form)
    newP = request.form['nameP']
    newPas = request.form['new_Pass']
    salted = bcrypt.hashpw( bytes(request.form['new_Pass'],  'utf-8' ) , bcrypt.gensalt(10))
    submit = "INSERT INTO users(username,password) VALUES('"
    submit += str (newP)
    submit += "','"
    submit += str (salted.decode('utf-8'))
    submit += "');"
    #print(submit)
    cur = global_db_con.cursor()
    cur.execute(submit)
    global_db_con.commit()
    return json_response(status='good',  message = 'New User')

def book_info (name_book):
    cur = global_db_con.cursor()
    book_r ="SELECT "
    book_r += name_book
    book_r += " FROM books;"
    print(book_r)

    cur = global_db_con.cursor()
    cur.execute(book_r)
    rp  = cur.fetchall()
    print(rp)
    return rp

def place_buybook (username, buybook_name, date_time):
    cur = global_db_con.cursor()
    receipt = "INSERT INTO purchases (username, buybook_name, date_time) VALUES( '"
    receipt += username
    receipt += "','"
    receipt += buybook_name
    receipt += "','"
    receipt += date_time
    receipt += "');"
    print(receipt)
    cur.execute(receipt)
    global_db_con.commit()



