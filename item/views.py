from venv import logger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from lxdong_proj2.permissions import IsAdminUser

class CategoryListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        category_model = Category()
        categories = category_model.get_all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryPostView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category_model = Category()
            category_id = category_model.create(serializer.validated_data['name'])
            category_data = category_model.get_by_id(category_id)
            category_serializer = CategorySerializer(category_data)
            return Response({"message": "Tạo category thành công", "data": category_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        item_model = Item()
        items = item_model.get_all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ItemPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            item_model = Item()
            item_id = item_model.create(
                name=serializer.validated_data['name'],
                price=serializer.validated_data['price'],
                description=serializer.validated_data['description'],
                category_id=serializer.validated_data['category_id'],
                image=serializer.validated_data.get('image'),
                quantity=serializer.validated_data.get('quantity', 0)
            )
            item_data = item_model.get_by_id(item_id)
            item_serializer = ItemSerializer(item_data)
            return Response({"message": "Tạo thành công sản phẩm", "data": item_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ItemDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        item_id = request.query_params.get('id')
        logger.info("item_id: %s", item_id)
        if not item_id:
            return Response({"error": "Thiếu tham số id"}, status=status.HTTP_400_BAD_REQUEST)
        item_model = Item()
        item = item_model.get_by_id(item_id)
        if item:
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Sản phẩm không tồn tại"}, status=status.HTTP_404_NOT_FOUND)