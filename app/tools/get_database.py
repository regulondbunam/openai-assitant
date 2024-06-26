import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def ping_mongodb(client):
   """
   Pings the MongoDB server to check the connection.

   Args:
      client (pymongo.MongoClient): The MongoDB client object.

   Returns:
      bool: True if the ping is successful, False otherwise.
   """
   try:
      client.admin.command('ping')
      return True
   except Exception:
      return False

def get_database():
   """
   Connects to MongoDB and returns the specified database.

   Returns:
      pymongo.database.Database: The MongoDB database object.
   """
   database = None
   try:
      MONGODB_CONNECTION_URI = os.environ['MONGODB_CONNECTION_URI']
   except KeyError:
      raise Exception("MONGODB_CONNECTION_URI environment variable is not set.")

   try:
      client = MongoClient(MONGODB_CONNECTION_URI)
      if ping_mongodb(client):
         database = client["chatbot"]
         print("Connected to MongoDB.")
      else:
         return None
   except Exception as e:
      raise Exception(f"Failed to connect to MongoDB: {str(e)}")

   return database
