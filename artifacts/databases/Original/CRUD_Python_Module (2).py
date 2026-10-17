# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username=None, password=None):
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = 'aacuser' 
        PASS = 'SNHU1234' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d/?authSource=%s' % (USER,PASS,HOST,PORT,DB)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)] 

    # Create a method to return the next available record number for use in the create method
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None: 
            try:
                self.database.animals.insert_one(data)  # data should be dictionary 
                return True
            except Exception as e:
                print(f"An error occurred while inserting: {e}")
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty") 

    # Create method to implement the R in CRUD..
    
    def read(self, query):
        """
        Query for documents in the collection.
        Input: a dictionary representing the key/value lookup pair.
        Returns: a list of matching documents if successful, else an empty list.
        """
        if query is not None:
            try:
                cursor = self.database.animals.find(query)
                result = list(cursor)
                return result
            except Exception as e:
                print(f"An error occurred while querying: {e}")
                return []
        else:
            raise Exception("Query parameter cannot be empty")
    
    # Create method to implement the U in CRUD.
    def update(self, query, update_data, update_many=False):
        """
        Query for document(s) in the collection and modify them.
        Input:
            query        -- a dictionary representing the key/value lookup pair
                             used to find the document(s) to update.
            update_data  -- a dictionary of key/value pairs, in the format
                             expected by MongoDB's update operators
                             
            update_many  -- optional boolean. If True, updates all matching
                             documents via update_many(). If False (default),
                             updates only the first matching document via
                             update_one().
        Returns: the number of documents modified in the collection. Returns
                 0 if no documents matched or if an error occurred.
        """
        if query is not None and update_data is not None:
            try:
                if update_many:
                    result = self.database.animals.update_many(query, update_data)
                else:
                    result = self.database.animals.update_one(query, update_data)
                return result.modified_count
            except Exception as e:
                print(f"An error occurred while updating: {e}")
                return 0
        else:
            raise Exception("Query and update_data parameters cannot be empty")
    
     # Create method to implement the D in CRUD.
    def delete(self, query, delete_many=False):
        """
        Query for document(s) in the collection and remove them.
        Input:
            query       -- a dictionary representing the key/value lookup pair
                            used to find the document(s) to delete.
            delete_many -- optional boolean. If True, removes all matching
                           documents via delete_many(). If False (default),
                           removes only the first matching document via
                           delete_one().
        Returns: the number of documents removed from the collection. Returns
                 0 if no documents matched or if an error occurred.
        """
        if query is not None:
            try:
                if delete_many:
                    result = self.database.animals.delete_many(query)
                else:
                    result = self.database.animals.delete_one(query)
                return result.deleted_count
            except Exception as e:
                print(f"An error occurred while deleting: {e}")
                return 0
        else:
            raise Exception("Query parameter cannot be empty")
            