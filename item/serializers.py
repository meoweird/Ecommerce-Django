from rest_framework import serializers
from bson import ObjectId

class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # Chuyển ObjectId thành string
    name = serializers.CharField(max_length=255)
    
    def to_representation(self, instance):
        """Chuyển đổi ObjectId thành chuỗi khi trả về JSON"""
        if isinstance(instance.get("_id"), ObjectId):
            instance["_id"] = str(instance["_id"])
        return super().to_representation(instance)

class ItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # Chuyển ObjectId thành string
    name = serializers.CharField(max_length=255)
    price = serializers.FloatField()
    description = serializers.CharField()
    category_id = serializers.CharField()
    image = serializers.CharField(allow_blank=True, required=False)
    quantity = serializers.IntegerField(default=0)

    def to_representation(self, instance):
        """Chuyển đổi ObjectId thành chuỗi khi trả về JSON"""
        if isinstance(instance.get("_id"), ObjectId):
            instance["_id"] = str(instance["_id"])
        if isinstance(instance.get("category_id"), ObjectId):
            instance["category_id"] = str(instance["category_id"])
        return super().to_representation(instance)