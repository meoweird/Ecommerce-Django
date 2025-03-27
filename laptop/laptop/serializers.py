from bson import ObjectId
from rest_framework import serializers

class LaptopSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    brand = serializers.CharField()
    processor = serializers.CharField()
    ram = serializers.CharField()
    storage = serializers.CharField()
    display = serializers.CharField()
    price = serializers.FloatField()
    stock = serializers.IntegerField()
    
    def to_representation(self, instance):
        if isinstance(instance.get("_id"), ObjectId):
            instance["_id"] = str(instance["_id"])
        return super().to_representation(instance)