import os
from dotenv import load_dotenv, dotenv_values
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = os.getenv("MONGODB_URL")

client = MongoClient(uri, server_api=ServerApi('1'))

db = client.todo_fast_api
collection = db['todo_data']  # collection todo_table
collection1 = db['waiting_table']  # collection1 = waiting table
