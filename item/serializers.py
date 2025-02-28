from rest_framework import serializers
from bson import ObjectId

from item.models import Item, Metadata

class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    metadata = serializers.ListField(child=serializers.CharField(), required=False, default=[])

    def to_representation(self, instance):
        if isinstance(instance.get("_id"), ObjectId):
            instance["_id"] = str(instance["_id"])
        return super().to_representation(instance)
    
# Metadata
class MetadataSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    category_id = serializers.CharField()
    fields = serializers.JSONField()

    def create(self, validated_data):
        metadata_model = Metadata()
        metadata_id = metadata_model.create(
            category_id=validated_data["category_id"],
            fields=validated_data["fields"]
        )
        return metadata_model.get_by_category(metadata_id)

class ItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    category_id = serializers.CharField()
    description = serializers.CharField()
    image = serializers.CharField(allow_null=True, required=False)
    metadata = serializers.JSONField(default=dict)
    variants = serializers.ListField(child=serializers.JSONField(), default=list)

    def create(self, validated_data):
        item_model = Item()
        item_id = item_model.create(
            name=validated_data['name'],
            category_id=validated_data['category_id'],
            description=validated_data['description'],
            image=validated_data.get('image', None),
            metadata=validated_data.get('metadata', {}),
            variants=validated_data.get('variants', [])
        )
        return item_model.get_by_id(item_id)