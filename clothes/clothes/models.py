from clothes import settings
from pymongo import MongoClient
from bson import ObjectId


class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]
        
class Clothes(MongoDB):
    def __init__(self):
        super().__init__()
        self.collection = self.db["clothes"]
        
    def create(self,clothes):
        self.collection.insert_one(clothes)
        
    def get_by_id(self,clothes_id):
        if not (ObjectId.is_valid(clothes_id)):
            return None
        return self.collection.find_one({"_id":ObjectId(clothes_id)})
    
    def get_all(self):
        return self.collection.find()
    
    def update(self,clothes_id,clothes):
        if not (ObjectId.is_valid(clothes_id)):
            return None
        self.collection.update_one({"_id":ObjectId(clothes_id)},{"$set":clothes})
        
    def delete(self,clothes_id):
        if not (ObjectId.is_valid(clothes_id)):
            return None
        self.collection.delete_one({"_id":ObjectId(clothes_id)})