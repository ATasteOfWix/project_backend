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

def POST(post, collection):
    collection = get_db()[collection]
    collection.insert_one(post)

def GET(collection, query = None): 
    collection = get_db()[collection]
    results = list(collection.find(query))
    for e in results:
        e['_id'] = str(e['_id'])
   
    results = dict(zip(range(len(results)),results)) 
    results['length'] = len(results)
    return json.dumps(results)

class User(Resource):
    def get(self): # for login function
        # GET /user?user_name=<xxx>&password=<xxx>
        user_name = request.args.get('user_name', '')
        password = request.args.get('password', '')

        user = GET({'user':user_name, 'password':password})

    def post(self): # for sign up function
        pass

app = Flask(__name__)
api = Api(app)

api.add_resource(User,'/user')

if __name__ == "__main__":
    user = {'user':'Boheng Luan','password':'987'}
    POST(user, 'user_profile')
    print(GET('user_profile'))

    app.run(port=5002)
