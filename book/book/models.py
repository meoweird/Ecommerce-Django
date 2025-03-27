from book import settings
from pymongo import MongoClient
from bson import ObjectId


class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]
        
class Book(MongoDB):
    def __init__(self):
        super().__init__()
        self.collection = self.db['books']
        
    def create(self,book):
        self.collection.insert_one(book)
        
    def get_by_id(self,book_id):
        if not (ObjectId.is_valid(book_id)):
            return None
        return self.collection.find_one({"_id":ObjectId(book_id)})
    
    def get_all(self):
        return self.collection.find()
    
    def update(self,book_id,book):
        if not (ObjectId.is_valid(book_id)):
            return None
        self.collection.update_one({"_id":ObjectId(book_id)},{"$set":book})
        
    def delete(self,book_id):
        if not (ObjectId.is_valid(book_id)):
            return None
        self.collection.delete_one({"_id":ObjectId(book_id)})