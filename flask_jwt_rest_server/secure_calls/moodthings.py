#cool

from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.tools_db import place_reason

from tools.logging import logger

def handle_request():
    logger.debug("Buy Books Handle Request")
   #print("hi")
    print(request.form['username'])
    print(request.form['users_moods'])
    print(request.form['date_time'])
    print(request.form['whymood'])
    place_reason(request.form['username'],request.form['users_moods'],request.form['date_time'],request.form['whymood'])

    #print(request.form['username'])
    #print(request.form['buybook_name'])
    #print(request.form['date_time'])

    return json_response( token = create_token(  g.jwt_data ) , moods = {})

    #return json_response( token = create_token(  g.jwt_data ) , books = {})
