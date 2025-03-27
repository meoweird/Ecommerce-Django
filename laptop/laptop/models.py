from pymongo import MongoClient
from bson import ObjectId

from laptop import settings

class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]
        
class Laptop(MongoDB):
    def __init__(self):
        super().__init__()
        self.collection = self.db["laptops"]
        
    def create(self,laptop):
        self.collection.insert_one(laptop)
        
    def get_by_id(self,laptop_id):
        if not (ObjectId.is_valid(laptop_id)):
            return None
        return self.collection.find_one({"_id":ObjectId(laptop_id)})
    
    def get_all(self):
        return self.collection.find()
    
    def update(self,laptop_id,laptop):
        if not (ObjectId.is_valid(laptop_id)):
            return None
        self.collection.update_one({"_id":ObjectId(laptop_id)},{"$set":laptop})
        
    def delete(self,laptop_id):
        if not (ObjectId.is_valid(laptop_id)):
            return None
        self.collection.delete_one({"_id":ObjectId(laptop_id)})