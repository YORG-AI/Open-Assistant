from src.core.nodes.base_node import BaseNode, NodeConfig
from src.utils.router_generator import generate_node_end_points
from .mongodb_model import (
    AggregateInput,
    DeleteInput,
    FindInput,
    FindReplaceInput,
    FindUpdateInput,
    InsertInput,
    UpdateInput,
)

from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
import os


mongodb_node_config = {
    "name": "mongodb",
    "description": "A node for MongoDB operations.",
    "functions": {
        "aggregate_documents": "Aggregate documents in a MongoDB collection.",
        "delete_documents": "Delete documents from a MongoDB collection.",
        "find_documents": "Find documents in a MongoDB collection.",
        "find_replace_documents": "Find and replace documents in a MongoDB collection.",
        "find_update_documents": "Find and update documents in a MongoDB collection.",
        "insert_documents": "Insert documents into a MongoDB collection.",
        "update_documents": "Update documents in a MongoDB collection.",
    },
}


@generate_node_end_points
class MongoDBNode(BaseNode):
    config: NodeConfig = NodeConfig(**mongodb_node_config)

    def __init__(self):
        super().__init__()
        uri = os.getenv("MONGODB_URI")
        # Here's your MongoDB connection setup.
        client = MongoClient(uri)
        self.db = client["yumiao-cluster"]

    def aggregate_documents(self, input: AggregateInput):
        collection = self.db[input.collection_name]
        result = list(collection.aggregate(input.pipeline))
        return result

    def delete_documents(self, input: DeleteInput):
        collection = self.db[input.collection_name]
        result = collection.delete_many(input.query)
        return {"deleted_count": result.deleted_count}

    def find_documents(self, input: FindInput):
        collection = self.db[input.collection_name]

        # Convert _id in query to ObjectId if it exists
        if "_id" in input.query:
            if isinstance(input.query["_id"], dict) and "$oid" in input.query["_id"]:
                input.query["_id"] = ObjectId(input.query["_id"]["$oid"])
            elif isinstance(input.query["_id"], str):
                try:
                    input.query["_id"] = ObjectId(input.query["_id"])
                except:
                    pass  # Invalid ObjectId format, proceed with the original query

        documents = list(collection.find(input.query))

        # Convert the ObjectId fields to strings for JSON serialization
        for document in documents:
            document["_id"] = str(document["_id"])

        return documents

    def find_replace_documents(self, input: FindReplaceInput):
        collection = self.db[input.collection_name]

        # Convert _id in filter to ObjectId if it exists
        if "_id" in input.filter:
            if isinstance(input.filter["_id"], dict) and "$oid" in input.filter["_id"]:
                input.filter["_id"] = ObjectId(input.filter["_id"]["$oid"])
            elif isinstance(input.filter["_id"], str):
                try:
                    input.filter["_id"] = ObjectId(input.filter["_id"])
                except:
                    pass  # Invalid ObjectId format, proceed with the original filter

        result = collection.find_one_and_replace(
            input.filter, input.replacement, return_document=ReturnDocument.AFTER
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    def find_update_documents(self, input: FindUpdateInput):
        collection = self.db[input.collection_name]

        # Convert _id in filter to ObjectId if it exists
        if "_id" in input.filter:
            if isinstance(input.filter["_id"], dict) and "$oid" in input.filter["_id"]:
                input.filter["_id"] = ObjectId(input.filter["_id"]["$oid"])
            elif isinstance(input.filter["_id"], str):
                try:
                    input.filter["_id"] = ObjectId(input.filter["_id"])
                except:
                    pass  # Invalid ObjectId format, proceed with the original filter

        result = collection.find_one_and_update(
            input.filter, {"$set": input.update}, return_document=ReturnDocument.AFTER
        )
        if result:
            result["_id"] = str(result["_id"])
        return result

    def insert_documents(self, input: InsertInput):
        collection = self.db[input.collection_name]
        result = collection.insert_many(input.documents)
        # Convert ObjectIds to strings
        inserted_ids = [str(_id) for _id in result.inserted_ids]
        return {"inserted_ids": inserted_ids}

    def update_documents(self, input: UpdateInput):
        collection = self.db[input.collection_name]

        # Convert _id in filter to ObjectId if it exists
        if "_id" in input.filter:
            if isinstance(input.filter["_id"], dict) and "$oid" in input.filter["_id"]:
                input.filter["_id"] = ObjectId(input.filter["_id"]["$oid"])
            elif isinstance(input.filter["_id"], str):
                try:
                    input.filter["_id"] = ObjectId(input.filter["_id"])
                except:
                    pass  # Invalid ObjectId format, proceed with the original filter

        result = collection.update_many(input.filter, {"$set": input.update})
        return {"modified_count": result.modified_count}
