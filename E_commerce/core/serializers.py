from rest_framework import serializers
from .models import Product

# chỉ dùng để trả về dữ liệu file JSON
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'image'] 