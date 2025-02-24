from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId

class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]

class Category(MongoDB):
    def __init__(self):
        super().__init__()
        self.collection = self.db['categories']

    def create(self, name):
        category = {"name": name}
        result = self.collection.insert_one(category)
        return str(result.inserted_id)
    
    def get_all(self):
        categories = list(self.collection.find())
        for category in categories:
            category["id"] = str(category["_id"])  
            del category["_id"]
        return categories

    def get_by_id(self, category_id):
        if not ObjectId.is_valid(category_id):
            return None
        category = self.collection.find_one({"_id": ObjectId(category_id)})
        if category:
            category["id"] = str(category["_id"])
            del category["_id"]
        return category

class Item(MongoDB):
    def __init__(self):
        super().__init__()
        self.collection = self.db['items']

    def create(self, name, price, description, category_id, image=None, quantity=0):
        if not ObjectId.is_valid(category_id):
            return None  
        item = {
            "name": name,
            "price": price,
            "description": description,
            "category_id": ObjectId(category_id),
            "image": image,
            "quantity": quantity
        }
        result = self.collection.insert_one(item)
        return str(result.inserted_id)

    def get_all(self):
        items = list(self.collection.find())
        for item in items:
            item["id"] = str(item["_id"])
            item["category_id"] = str(item["category_id"]) if "category_id" in item else None
            del item["_id"] 
        return items

    def get_by_id(self, item_id):
        if not ObjectId.is_valid(item_id):
            return None
        item = self.collection.find_one({"_id": ObjectId(item_id)})
        if item:
            item["id"] = str(item["_id"])
            item["category_id"] = str(item["category_id"]) if "category_id" in item else None
            del item["_id"]
        return item

    def update(self, item_id, update_data):
        if not ObjectId.is_valid(item_id):
            return None
        return self.collection.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})

    def delete(self, item_id):
        if not ObjectId.is_valid(item_id):
            return None
        return self.collection.delete_one({"_id": ObjectId(item_id)})
