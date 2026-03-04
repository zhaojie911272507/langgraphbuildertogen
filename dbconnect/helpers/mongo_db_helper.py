from ..utils.mongo_db_utils import CRUDOperations


class CRUDHelper(CRUDOperations):
    # def __init__(self, bu_name, data_model):
    #     super().__init__(bu_name, collection_name=data_model.Config.collection)
    #     self.data_model = data_model

    def __init__(self, data_model):
        super().__init__(collection_name=data_model.Config.collection)
        self.data_model = data_model

    async def create(self, data):
        return await self.create_document(document=data.dict())

    async def read(self, query):
        return await self.read_document(query=query)

    async def update(self, query, update_data):
        return await self.update_document(query=query, update_data=update_data)

    async def delete(self, query):
        return await self.delete_document(query=query)

