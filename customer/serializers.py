from rest_framework import serializers
from .models import Customer

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'phone','first_name', 'last_name' , 'password']

    def create(self, validated_data):
        user = Customer.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data.get('phone', ''),
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user