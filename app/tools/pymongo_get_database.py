import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
DATABASE_NAME = os.environ['DATABASE_NAME']

def get_database():
   """
   Connects to MongoDB and returns the specified database.

   Returns:
      pymongo.database.Database: The MongoDB database object.
   """
   MONGODB_CONNECTION_URI = os.environ['MONGODB_CONNECTION_URI']

   client = MongoClient(MONGODB_CONNECTION_URI)

   return client[DATABASE_NAME]
  
if __name__ == "__main__":   
  
   dbname = get_database()