from laptop.models import Laptop
from laptop.serializers import LaptopSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LaptopList(APIView):
    def get(self,request):
        laptop = Laptop()
        all_laptop = laptop.get_all()
        serializer = LaptopSerializer(all_laptop,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = LaptopSerializer(data=request.data)
        if serializer.is_valid():
            laptop = Laptop()
            laptop.create(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LaptopDetail(APIView):
    def get(self,request,laptop_id):
        laptop = Laptop()
        laptop = laptop.get_by_id(laptop_id)
        if laptop:
            serializer = LaptopSerializer(laptop)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,laptop_id):
        serializer = LaptopSerializer(data=request.data)
        if serializer.is_valid():
            laptop = Laptop()
            laptop.update(laptop_id,serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,laptop_id):
        laptop = Laptop()
        laptop.delete(laptop_id)
        return Response(status=status.HTTP_204_NO_CONTENT)