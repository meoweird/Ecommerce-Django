from book.models import Book
from book.serializers import BookSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BookList(APIView):
    def get(self,request):
        book = Book()
        books = book.get_all()
        serializer = BookSerializer(books,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = Book()
            book.create(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class BookDetail(APIView):
    def get(self,request,book_id):
        book = Book()
        book = book.get_by_id(book_id)
        if book:
            serializer = BookSerializer(book)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,book_id):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = Book()
            book.update(book_id,serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,book_id):
        book = Book()
        book.delete(book_id)
        return Response(status=status.HTTP_204_NO_CONTENT)