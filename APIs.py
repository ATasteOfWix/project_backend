from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import json
import pymongo  # pip install pymongo
from bson import json_util 
from pymongo import MongoClient# Comes with pymongo

print('package loaded!')

def get_db():
    try:
        client = MongoClient('mongodb://admin:Gh1QyOay3xC1@localhost:27017')
        db = client['admin']
        return db
    except:
        print('Error: unable to connect mongodb!')
        return None

def POST(collection, post):
    collection = get_db()[collection]
    collection.insert_one(post)

def GET(collection, query = None): 
    collection = get_db()[collection]
    results = list(collection.find(query))
    for e in results:
        e['_id'] = str(e['_id'])
   
    results = dict(zip(range(len(results)),results)) 
    results['length'] = len(results)
    return results

class Session_token:
    def __init__(self):


class Test(Resource):
    def get(self, arg):
        return json.dumps({'message':'connection established!', 'arg':arg})

class Login(Resource):
    def get(self, user_name, password): # for login function
        print('#debug print:', (user_name, password))
        user = GET('user_profile', {'user':user_name, 'password':password})
        return 

class Sign_up(Resource):
    def get(self, user_name, password, email):
        print('#debug print:', (user_name, password))
        user = {'user':user_name, 'password':password, 'email':email}
        user_exist = GET('user_profile',user)['length'] != 0
        print('#debug print: user exist', GET('user_profile',user), user_exist) 
        if user_exist:
            return 'user already exist!'
        else:
            POST('user_profile',user)
            return 'sign up successful!'


app = Flask(__name__)
api = Api(app)

api.add_resource(Test,'/test/<arg>')
api.add_resource(Login,'/login/<user_name>/<password>')
api.add_resource(Sign_up,'/signup/<user_name>/<password>/<email>')

if __name__ == "__main__":
    app.run('115.146.92.114',port=8888)

