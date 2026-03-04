# -*- coding: utf-8 -*-
import asyncio
import json
import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
# from app.controllers import mongo_decorator
from dotenv import dotenv_values
from pathlib import Path

# from app.config import ASD_CONFIG, CGO_CONFIG
from logger_utils import log_with_trace_id


class MongoDBUtils:
    def __init__(self):
        # self.bu_name = bu_name
        # self.bu_config = {
        #     "ASD": ASD_CONFIG,
        #     "CGO": CGO_CONFIG
        # }
        # Retrieve MongoDB connection details from configuration
        # self.username, self.password, self.DB_NAME, self.slice_a, self.slice_b, self.slice_c = self.bu_config[bu_name].mongodb_config.initial_connect_config()
        # self.username, self.password, self.DB_NAME, self.slice_a = self.bu_config[
        #     bu_name].mongodb_config.initial_connect_config()

        self.username = os.getenv("MONGO_USER")
        self.password = os.getenv("MONGO_PASSWORD")
        self.DB_NAME = os.getenv("MONGO_DB_NAME")
        self.slice_a = os.getenv("MONGO_SLICE_A")
        self.client = None
        self.db = None


    async def create_client(self, server_selection_timeout=5000, connect_timeout=5000):
        # Create the MongoDB client connection URL
        DATABASE_URL = (
            f"mongodb://{self.username}:{self.password}@"
            # f"{self.slice_a},"
            # f"{self.slice_b},"
            f"{self.slice_a}/"
            f"?authMechanism=DEFAULT&tls=true&tlsAllowInvalidHostnames=true&"
            f"serverSelectionTimeoutMS={server_selection_timeout}&connectTimeoutMS={connect_timeout}"
        )
        print(DATABASE_URL)
        # Initialize the async MongoDB client
        client = AsyncIOMotorClient(DATABASE_URL)
        return client

    async def initialize_db(self):
        # Initialize the database connection
        if self.client is None:
            self.client = await self.create_client()
        if self.db is None:
            self.db = self.client[self.DB_NAME]
        return self.db

    async def close(self):
        # Close the MongoDB client
        if self.client:
            self.client.close()

    # Add __aenter__ and __aexit__ to support async context manager for automatic closing
    async def __aenter__(self):
        # Return the client to be used in a 'with' statement
        await self.initialize_db()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # Ensure the client is closed when exiting the context
        await self.close()

    def start_event_loop(self, loop=None):
        """ Ensure the event loop is running """
        if loop is None:
            loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop

    def stop_event_loop(self, loop=None):
        """ Ensure the event loop is properly closed """
        if loop:
            loop.stop()
            loop.close()

class MongoDBCollectionManager(MongoDBUtils):
    def __init__(self,  collection_name, intent_name, sub_intent_name, json_file_name):
        super().__init__()
        # self.json_file_path = self.bu_config[bu_name].bu_datasets_config.init_json_file_path(intent_name=intent_name, json_file_name=json_file_name,sub_intent_name=sub_intent_name)
        # self.collection_schema = self.bu_config[bu_name].bu_datasets_config.select_collection_schema(intent_name=intent_name)

        self.json_file_path = None
        self.collection_schema = None
        self.collection_name = collection_name

    async def check_and_initialize_collection(self):
        """
        checking collection is exist, clear and initialize again
        """
        # get connect link
        db = await self.initialize_db()
        collection = db[self.collection_name]

        # checking collection if it is exists
        collection_exists = self.collection_name in await db.list_collection_names()
        if collection_exists:
            log_with_trace_id(message=f"Collection '{self.collection_name}' already had one，deleting and rebuilding...", open_trace_id=False)
            await collection.drop()

        # rebuild collection
        log_with_trace_id(message=f"create a new Collection '{self.collection_name}'...", open_trace_id=False)
        try:
            await self.db.create_collection(
                name=self.collection_name,
                validator=self.collection_schema
            )
        except Exception as e:
            log_with_trace_id(message=f"Failed to create collection: {str(e)}", open_trace_id=False)
            raise
        return collection

    async def load_json_data(self):
        """
        read data from Json file in local environment
        """
        log_with_trace_id(message=f"From json file '{self.json_file_path}' loading data...", open_trace_id=False)
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # confirm data format is list
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            raise ValueError("JSON file content must be dict or list format")
        
        log_with_trace_id(message=f"loaded {len(data)} items successfully!", open_trace_id=False)
        return data

    async def import_data(self, collection: AsyncIOMotorCollection, data: list):
        """
        import data to the specific collection
        """
        log_with_trace_id(message=f"import data to Collection '{self.collection_name}'...", open_trace_id=False)
        await collection.insert_many(data)
        log_with_trace_id(message=f"Dataset import finished，number of sum is {len(data)} items")

    async def initialize_data(self):
        """
        all process logics: checking\cleaning\creating\loading
        """
        # checking collection and rebuilding
        collection = await self.check_and_initialize_collection()

        # loading JSON data
        data = await self.load_json_data()

        # import data to the collection
        await self.import_data(collection, data)

class CRUDOperations(MongoDBUtils):
    def __init__(self, collection_name):
        super().__init__()
        self.collection_name = collection_name
        self.db = None
        self.collection = None

    async def initialize(self):
        """ Initialize the database connection and collection """
        if self.db is None:
            self.db = await self.initialize_db()  # Get database connection
        self.collection = self.db[self.collection_name]  # Get collection
        return self.collection

    async def create_document(self, document):
        """ Create a document in the collection """
        try:
            collection = await self.initialize()
            result = await collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            raise

    async def read_document(self, query):
        """ Read a document from the collection """
        try:
            collection = await self.initialize()
            document = await collection.find_one(query)
            return document
        except Exception as e:
            raise

    async def read_documents(self):
        """Read multiple documents from the collection"""
        try:
            collection = await self.initialize()
            cursor = collection.find({},{"_id": 0, "_initialized":0})  # find multi-documents
            documents = []
            async for document in cursor:
                documents.append(document)
            return documents
        except Exception as e:
            raise Exception(f"An error occurred while reading documents: {e}")

    async def condition_search_documents(self, query):
        """Search for documents in the collection"""
        try:
            collection = await self.initialize()
            cursor = collection.find(query)
            documents = []
            async for document in cursor:
                documents.append(document)
            return documents
        except Exception as e:
            raise Exception(f"An error occurred while searching documents: {e}")

    async def get_description_info(self):
        """Get descriptions of the fields and collection schema"""
        try:
            # Retrieve collection schema (validation rules)
            collection = await self.initialize()
            collection_options = await collection.options()
            log_with_trace_id(message=f"{collection_options}", open_trace_id=False)
            schema = collection_options.get("validator", {}).get('$jsonSchema', {})
            log_with_trace_id(message=f"schema is {schema}", open_trace_id=False)
            # Extract collection description
            collection_description = schema.get('description', 'No collection description available')
            log_with_trace_id(message=f"collection description is {collection_description}", open_trace_id=False)
            # Extract field descriptions from the schema
            field_descriptions = {}
            if schema and 'properties' in schema:
                for field, field_info in schema['properties'].items():
                    description = field_info.get('description', 'No description available')
                    field_descriptions[field] = description

            # Return both collection description and field descriptions
            return {
                'collection_description': collection_description,
                'field_descriptions': field_descriptions
            }
        except Exception as e:
            raise Exception(f"Failed to get collection and field descriptions: {e}")

    async def update_document(self, query, update_data):
        """ Update a document in the collection """
        try:
            collection = await self.initialize()
            result = await collection.update_one(query, {'$set': update_data})
            return result.modified_count
        except Exception as e:
            raise

    async def delete_document(self, query):
        """ Delete a document from the collection """
        try:
            collection = await self.initialize()
            result = await collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            raise


client = MongoDBUtils()
print(client)