from clothes.models import Clothes
from clothes.serializers import ClothesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ClothesList(APIView):
    def get(self,request):
        clothes = Clothes()
        all_clothes = clothes.get_all()
        serializer = ClothesSerializer(all_clothes,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ClothesSerializer(data=request.data)
        if serializer.is_valid():
            clothes = Clothes()
            clothes.create(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ClothesDetail(APIView):
    def get(self,request,clothes_id):
        clothes = Clothes()
        clothes = clothes.get_by_id(clothes_id)
        if clothes:
            serializer = ClothesSerializer(clothes)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,clothes_id):
        serializer = ClothesSerializer(data=request.data)
        if serializer.is_valid():
            clothes = Clothes()
            clothes.update(clothes_id,serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,clothes_id):
        clothes = Clothes()
        clothes.delete(clothes_id)
        return Response(status=status.HTTP_204_NO_CONTENT)