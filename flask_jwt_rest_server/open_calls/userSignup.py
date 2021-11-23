#open_calls
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger
import bcrypt
import jwt
from db_con import get_db_instance, get_db

global_db_con = get_db()




def handle_request ():
    print(request.form)
    newP = request.form['firstname']
    newPas = request.form['password']
    salted = bcrypt.hashpw( bytes(request.form['password'],  'utf-8' ) , bcrypt.gensalt(10))
    submit = "INSERT INTO users(username,password) VALUES('"
    submit += str (newP)
    submit += "','"
    submit += str (salted.decode('utf-8'))
    submit += "');"
    #print(submit)
    print(newP)
    print(newPas)
    cur = global_db_con.cursor()
    cur.execute(submit)
    global_db_con.commit()
    return json_response(status='good',  message = 'New User')
