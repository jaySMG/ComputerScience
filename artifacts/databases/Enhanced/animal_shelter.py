"""
Database access module for the Grazioso Salvare Rescue Animal Dashboard.

The AnimalShelter class provides CRUD operations, aggregation, and index
management for animal records stored in MongoDB.
"""

import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class AnimalShelter:
    """Manage MongoDB operations for the animal shelter collection."""

    def __init__(self):
        """Initialize the MongoDB connection and animal collection."""

        # Load connection settings from environment variables.
        host = os.getenv("AAC_HOST", "localhost")
        port = int(os.getenv("AAC_PORT", "27017"))
        database_name = os.getenv("AAC_DB", "aac")
        collection_name = os.getenv("AAC_COLLECTION", "animals")

        # Connect to MongoDB and select the configured collection.
        self.client = MongoClient(host, port)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    def create(self, data):
        """
        Insert a new animal record into the collection.

        Args:
            data (dict): Animal record to insert.

        Returns:
            bool: True when the record is inserted successfully,
            otherwise False.

        Raises:
            ValueError: If data is not a non-empty dictionary.
        """

        if not isinstance(data, dict) or not data:
            raise ValueError(
                "Animal data must be provided as a non-empty dictionary."
            )

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
            list: Matching animal records.

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

    def aggregate(self, pipeline):
        """
        Run a MongoDB aggregation pipeline.

        Args:
            pipeline (list): MongoDB aggregation stages.

        Returns:
            list: Results produced by the aggregation pipeline.

        Raises:
            ValueError: If pipeline is not a non-empty list.
        """

        if not isinstance(pipeline, list) or not pipeline:
            raise ValueError(
                "Aggregation pipeline must be provided as a non-empty list."
            )

        try:
            return list(self.collection.aggregate(pipeline))
        except Exception as error:
            print(f"Unable to complete aggregation: {error}")
            return []

    def get_breed_counts(self, query=None):
        """
        Count breeds using a MongoDB aggregation pipeline.

        Args:
            query (dict, optional): Criteria used to limit records before
                grouping them by breed.

        Returns:
            list: Breed names and their record counts.

        Raises:
            ValueError: If query is not a dictionary.
        """

        if query is None:
            query = {}

        if not isinstance(query, dict):
            raise ValueError("Breed count query must be a dictionary.")

        pipeline = []

        if query:
            pipeline.append({"$match": query})

        pipeline.extend([
            {
                "$match": {
                    "breed": {
                        "$exists": True,
                        "$nin": [None, ""]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$breed",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {
                    "count": -1,
                    "_id": 1
                }
            }
        ])

        results = self.aggregate(pipeline)

        return [
            {
                "breed": result["_id"],
                "count": result["count"]
            }
            for result in results
        ]

    def create_indexes(self):
        """
        Create indexes for fields commonly used by rescue queries.

        Returns:
            list: Names of the indexes created or already present.
        """

        try:
            index_names = [
                self.collection.create_index("animal_type"),
                self.collection.create_index("breed"),
                self.collection.create_index("sex_upon_outcome"),
                self.collection.create_index("age_upon_outcome_in_weeks")
            ]

            return index_names

        except Exception as error:
            print(f"Unable to create database indexes: {error}")
            return []

    def get_indexes(self):
        """
        Retrieve the indexes currently defined for the collection.

        Returns:
            dict: MongoDB index definitions.

        Returns an empty dictionary if the index information
        cannot be retrieved.
        """

        try:
            return self.collection.index_information()

        except Exception as error:
            print(f"Unable to retrieve database indexes: {error}")
            return {}