from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.tools_db import check_password

from tools.logging import logger
import bcrypt
#import jwt
from db_con import get_db_instance, get_db

global_db_con = get_db()

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user

    password_from_user_form = request.form['password']
    user_form = request.form['firstname']

    print(password_from_user_form)
    print(user_form)
    if check_password(password_from_user_form, user_form) == True:

        user = {
                "sub" : request.form['firstname'] #sub is used by pyJwt as the owner of the token
                #"sub" : request.form['nameUser'] #sub is used by pyJwt as the owner of the token
                }
    else:
        user = False

    if not user:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )

    return json_response( token = create_token(user) , username = user_form  ,authenticated = True)

#def check_password(password,username):
    
 #   cur = global_db_con.cursor()
 #   if check_person(username) == False:
 #       return False
 #   pName = "SELECT password FROM users WHERE username ='"
 #   pName += request.form['firstname']
 #   pName += "';"
 #   print(pName)
 #   cur.execute(pName)
 #   r = cur.fetchone()
 #   user_Password = str(r[0])
 #   if bcrypt.checkpw(bytes(request.form['password'],'utf-8'), user_Password.encode('utf-8')):
 #       return True
 #   return False

#def check_person(username):
 #   cur = global_db_con.cursor()
 #   user_db = "SELECT EXISTS (SELECT username FROM users WHERE username = '"
 #   user_db += username
 #   user_db += "' limit 1)"
 #   print(user_db)
 #   cur.execute(user_db)
 #   r = cur.fetchone()
 #   print(r[0])
 #   if r[0] == True:
 #       return True
 #   return False

#def createPerson ():
  #  print(request.form)
  #  newP = request.form['nameP']
  #  newPas = request.form['new_Pass']
  #  salted = bcrypt.hashpw( bytes(request.form['new_Pass'],  'utf-8' ) , bcrypt.gensalt(10))
  #  submit = "INSERT INTO users(username,password) VALUES('"
  #  submit += str (newP)
  #  submit += "','"
  #  submit += str (salted.decode('utf-8'))
  #  submit += "');"
    #print(submit)
  #  cur = global_db_con.cursor()
  #  cur.execute(submit)
  #  global_db_con.commit()
  #  return json_response(status='good',  message = 'New User')
