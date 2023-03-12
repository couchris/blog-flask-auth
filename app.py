from flask import Flask, request, jsonify
import pymongo
import bcrypt
from pymongo import MongoClient
from flask import Markup
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
import ssl
from bson import json_util
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras

app = Flask(__name__)
load_dotenv()
MONGO_URi = os.environ.get('MONGO_URi')

def connectDB():
  try:
    # Set up a connection to the database - 'postgres://nszjufuw:eo-PTwUUTFjpo3kKUbGGOdoyDuGKmDeS@isilo.db.elephantsql.com/nszjufuw+psycopg2'
    conn = psycopg2.connect(
        dbname="nszjufuw",
        user="nszjufuw",
        password="eo-PTwUUTFjpo3kKUbGGOdoyDuGKmDeS",
        host="isilo.db.elephantsql.com"
    )
    return conn
  except:
    print("error cant connect to db")


@app.route('/register', methods=['POST'])
def startpy():
    try:
      username = request.json['username']
      password = request.json['password']
      password_bytes = password.encode('utf-8')
      hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
      user_tuple = (username, hashed_password)
      conn = connectDB()
      cur = conn.cursor()
      cur.execute("INSERT INTO _users (username, password) VALUES (%s, %s) RETURNING id, username", user_tuple)
      new_user = cur.fetchone()
      conn.commit()
      cur.close()
      conn.close()
      new_list = list(new_user)
      return jsonify(new_list)
    except Exception as err:
       print(err)
       return "err"
    return "success"

@app.route('/login', methods=['POST'])
def startpy2():
    username = request.json['username']
    password = request.json['password']
    print(type(username))
    conn = connectDB()
    cur = conn.cursor()
    cur.execute("SELECT username, password FROM _USERS WHERE username LIKE %s", (username, ))
    foundUser = cur.fetchone()
    print(foundUser)
    conn.commit()
    cur.close()
    conn.close()
    
    if foundUser:
      if bcrypt.checkpw(b'password', b'foundUser[1]'):
         foundUser[1] = ""
      
    new_list = list(foundUser)
    return jsonify(new_list)


if __name__ == '__main__':
  app.run(debug=True)