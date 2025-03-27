from rest_framework import serializers
from bson import ObjectId

class BookSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    author = serializers.CharField()
    year = serializers.IntegerField()
    description = serializers.CharField()
    price = serializers.FloatField()
    stock = serializers.IntegerField()
    
    def to_representation(self, instance):
        if isinstance(instance.get("_id"), ObjectId):
            instance["_id"] = str(instance["_id"])
        return super().to_representation(instance)