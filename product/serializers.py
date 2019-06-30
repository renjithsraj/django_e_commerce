from rest_framework import serializers
from product.models import  Products


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'slug', 'name')
