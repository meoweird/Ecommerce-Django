from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item, Category, Metadata
from .serializers import ItemSerializer, CategorySerializer, MetadataSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from lxdong_proj2.permissions import IsAdminUser

class CategoryListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        category_model = Category()
        metadata_model = Metadata()
        
        categories = category_model.get_all()
        for category in categories:
            metadata = metadata_model.get_by_category(category["id"])
            category["metadata"] = metadata["fields"] if metadata else []

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CategoryDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request ):
        category_id = request.query_params.get('id')
        category_model = Category()
        metadata_model = Metadata()

        category = category_model.get_by_id(category_id)
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        metadata = metadata_model.get_by_category(category_id)
        category["metadata"] = metadata["fields"] if metadata else []

        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryCreateView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category_model = Category()
            metadata_model = Metadata()

            # Tạo category mới
            category_id = category_model.create(serializer.validated_data['name'])
            category_data = category_model.get_by_id(category_id)

            # Nhận metadata từ request hoặc tạo metadata mặc định
            metadata_fields = request.data.get("metadata", [])
            metadata_id = metadata_model.create(category_id, metadata_fields)
            metadata_data = metadata_model.get_by_category(category_id)
            
            # Gán metadata cho category
            category_data["metadata"] = metadata_data["fields"]

            return Response({
                "message": "Tạo category thành công",
                "category": CategorySerializer(category_data).data,
                "metadata": MetadataSerializer(metadata_data).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        item_model = Item()
        items = item_model.get_all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ItemCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            return Response(ItemSerializer(item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        item_id = request.query_params.get('id')
        if not item_id:
            return Response({"error": "Thiếu tham số id"}, status=status.HTTP_400_BAD_REQUEST)
        item_model = Item()
        item = item_model.get_by_id(item_id)
        if item:
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Sản phẩm không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
    
# class MetadataView(APIView):
#     def get(self, request, category_id):
#         metadata_model = Metadata()
#         metadata = metadata_model.get_by_category(category_id)
#         if metadata:
#             serializer = MetadataSerializer(metadata)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({"error": "Metadata không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

#     def post(self, request):
#         serializer = MetadataSerializer(data=request.data)
#         if serializer.is_valid():
#             metadata = serializer.save()
#             return Response(MetadataSerializer(metadata).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)