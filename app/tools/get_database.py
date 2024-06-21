import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_database():
   """
   Connects to MongoDB and returns the specified database.

   Returns:
      pymongo.database.Database: The MongoDB database object.
   """
   try:
      MONGODB_CONNECTION_URI = os.environ['MONGODB_CONNECTION_URI']
   except KeyError:
      raise Exception("MONGODB_CONNECTION_URI environment variable is not set.")

   try:
      client = MongoClient(MONGODB_CONNECTION_URI)
      cliente = client["chatbot"]
   except Exception as e:
      raise Exception(f"Failed to connect to MongoDB: {str(e)}")

   return cliente