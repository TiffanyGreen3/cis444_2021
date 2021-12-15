from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.tools_db import mood_info
from tools.logging import logger
from db_con import get_db_instance, get_db

global_db_con = get_db()

def handle_request():
    logger.debug("Get Books Handle Request")

    #print("HERE are the books")

    #books_Price_resp = cur.fetchall()
    #print(books_Price_resp)
    nameMoods = mood_info("type_moods")
    #print(nameMoods)
    

    return json_response( token = create_token(  g.jwt_data ) , moods_Name_resp = nameMoods)
