"""
Database access module for the Grazioso Salvare Rescue Animal Dashboard.

The AnimalShelter class provides CRUD operations for animal records
stored in MongoDB.
"""

import os

from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv() 

class AnimalShelter:
    """Manage MongoDB operations for the animal shelter collection."""

    def __init__(self):
        """Initialize the MongoDB connection and animal collection."""

        # Load connection settings from environment variables.
        HOST = os.getenv("AAC_HOST", "localhost")
        PORT = int(os.getenv("AAC_PORT", "27017"))
        DB = os.getenv("AAC_DB", "aac")
        COL = os.getenv("AAC_COLLECTION", "animals")

        # Connect to MongoDB and select the configured collection.
        self.client = MongoClient(HOST, PORT)
        self.database = self.client[DB]
        self.collection = self.database[COL] 

   
    def create(self, data):
         """
        Insert a new animal record into the collection.

        Args:
            data (dict): Animal record to insert.

        Returns:
            bool: True when the record is inserted successfully, otherwise False.

        Raises:
            ValueError: If data is not a non-empty dictionary.
        """
         if not isinstance(data, dict) or not data:
             raise ValueError("Animal data must be provided as a non-empty dictionary.")

         try:
             self.collection.insert_one(data)
             return True
         except Exception as error:
             print(f"Unable to insert animal record: {error}")
             return False 
    
    def read(self, query):
        """
        Retrieve animal records that match the provided query.

        Args:
            query (dict): MongoDB query used to find matching records.

        Returns:
            list: Matching animal records. Returns an empty list when
            no records are found or if the query cannot be completed.

        Raises:
            ValueError: If query is not a dictionary.
        """

        if not isinstance(query, dict):
            raise ValueError("Query must be provided as a dictionary.")

        try:
            return list(self.collection.find(query))
        except Exception as error:
            print(f"Unable to retrieve animal records: {error}")
            return []
    
    
    def update(self, query, update_data, update_many=False):
        """
        Update one or more animal records that match the provided query.

        Args:
            query (dict): MongoDB query used to select records.
            update_data (dict): MongoDB update operation to apply.
            update_many (bool): If True, update all matching records.
                If False, update only the first matching record.

        Returns:
            int: Number of records modified.

        Raises:
            ValueError: If query or update_data is not a non-empty dictionary.
        """

        if not isinstance(query, dict) or not query:
            raise ValueError("Update query must be a non-empty dictionary.")

        if not isinstance(update_data, dict) or not update_data:
            raise ValueError("Update data must be a non-empty dictionary.")

        try:
            if update_many:
                result = self.collection.update_many(query, update_data)
            else:
                result = self.collection.update_one(query, update_data)

            return result.modified_count

        except Exception as error:
            print(f"Unable to update animal record(s): {error}")
            return 0
    
    
    def delete(self, query, delete_many=False):
        """
        Delete one or more animal records that match the provided query.

        Args:
            query (dict): MongoDB query used to select records.
            delete_many (bool): If True, delete all matching records.
                If False, delete only the first matching record.

        Returns:
            int: Number of records deleted.

        Raises:
            ValueError: If query is not a non-empty dictionary.
        """

        if not isinstance(query, dict) or not query:
            raise ValueError("Delete query must be a non-empty dictionary.")

        try:
            if delete_many:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)

            return result.deleted_count

        except Exception as error:
            print(f"Unable to delete animal record(s): {error}")
            return 0
            