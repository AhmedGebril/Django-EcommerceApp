from rest_framework import serializers
from .models import client,Review,Product,Order
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from rest_framework import validators


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = client
        fields = '__all__'
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
            "email": {
                "allow_blank": False,
                "required": True,
                "validators": [
                    validators.UniqueValidator(client.objects.all(), " Email already exists")
                ]
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        user = client.objects.create(password=hashed_password, **validated_data)
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'