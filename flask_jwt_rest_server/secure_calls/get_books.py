from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.tools_db import book_info
from tools.logging import logger
from db_con import get_db_instance, get_db

global_db_con = get_db()

def handle_request():
    logger.debug("Get Books Handle Request")

    print("HERE are the books")

    #cur = global_db_con.cursor()  
    #books_Name_request = "SELECT book_name FROM books;"
    #cur.execute(books_Name_request)
    #books_Name_resp = cur.fetchall()
    #print(books_Name_resp)

    #books_Price_request = "SELECT book_price FROM books;"
    #cur.execute(books_Price_request)
    #books_Price_resp = cur.fetchall()
    #print(books_Price_resp)
    nameBooks = book_info("book_name")
    priceBook = book_info("book_price")
    

    return json_response( token = create_token(  g.jwt_data ) , books_Name_resp = nameBooks, books_Price_resp = priceBook)

    #return json_response( token = create_token(  g.jwt_data ) , books = {})

