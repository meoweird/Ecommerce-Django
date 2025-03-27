from rest_framework import serializers
from bson import ObjectId

class ClothesSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    brand = serializers.CharField()
    color = serializers.CharField()
    size = serializers.CharField()
    price = serializers.FloatField()
    stock = serializers.IntegerField()
    
    def to_representation(self, instance):
        if isinstance(instance.get("_id"), ObjectId):
            instance["_id"] = str(instance["_id"])
        return super().to_representation(instance)
    