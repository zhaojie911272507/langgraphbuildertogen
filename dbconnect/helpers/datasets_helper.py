import asyncio

from ..utils.mongo_db_utils import MongoDBCollectionManager
from ..utils.mongo_db_utils import CRUDOperations
from ..utils.logger_utils import log_with_trace_id


async def initialize_data_once(collection_name, intent_name, json_file_name, sub_intent_name):
    async with MongoDBCollectionManager(collection_name, intent_name=intent_name,
                                        sub_intent_name=sub_intent_name, json_file_name=json_file_name) as manager:
        db = await manager.initialize_db()
        collection = db[collection_name]

        # First, check if the collection is already initialized
        initialized = await collection.find_one({"_initialized": True})
        if initialized:
            log_with_trace_id(message=f"Collection {collection_name} already initialized, skipping initialization.")
            return

        try:
            log_with_trace_id(message=f"Beginning initialization of collection: {collection_name}...")
            await manager.initialize_data()

            # After successful initialization, set the _initialized flag to True
            result = await collection.update_one(
                {"_initialized": {"$exists": False}},  # Ensure that we only update documents that are not initialized
                {"$set": {"_initialized": True}},
                upsert=True  # Create the _initialized flag if it doesn't exist
            )

            # Check if the update was successful
            if result.modified_count > 0:
                log_with_trace_id(message=f"Collection {collection_name} dataset initialization finished!")
            else:
                log_with_trace_id(message=f"Failed to set _initialized flag for collection {collection_name}.")

        finally:
            # Release the lock after the initialization is complete
            await collection.update_one(
                {"_initialized_lock": True},  # Lock is active
                {"$unset": {"_initialized_lock": ""}}  # Remove the lock
            )
            log_with_trace_id(message=f"Lock released for collection {collection_name}.")


class BuDataHelper(CRUDOperations):

    # def __init__(self, bu_name, data_model) -> None:
    #     super().__init__(bu_name, collection_name=data_model.Config.collection)

    def __init__(self, data_model) -> None:
        super().__init__(collection_name=data_model.Config.collection)

    async def read_all_data(self):
        return await self.read_documents()

    async def get_all_description(self):
        return await self.get_description_info()


class MetaDataHelper(CRUDOperations):

    def __init__(self, data_model) -> None:
        super().__init__(collection_name=data_model.Config.collection)

    async def search_all_data(self, query):
        return await self.condition_search_documents(query)









