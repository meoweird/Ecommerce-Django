from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ChangePasswordSerializer, CustomerDetailSerializer, CustomerRegistrationSerializer, CustomerUpdateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class CustomerRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Đăng ký thành công'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyTokenView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        token = request.data.get('token')
        try:
            decoded_token = AccessToken(token)
            return Response(decoded_token.payload, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Token không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Đăng xuất thành công"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CustomerUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = CustomerUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user_data = CustomerDetailSerializer(user).data
            return Response({'message': 'Cập nhật thông tin thành công', 'data': user_data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Sai mật khẩu cũ."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "Đổi mật khẩu thành công"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
