from rest_framework import serializers

from django.utils.text import slugify

from .models import Category, Product, PageContent, TeamMember, Comment, Customer




class CategorySerializer(serializers.ModelSerializer):
    num_of_products = serializers.IntegerField(source='products.count', read_only=True)
    
    class Meta:
        model = Category
        fields = ["id", "name", "description", "num_of_products"]

    def validate(self, data):
        if len(data['name']) < 3:
            raise serializers.ValidationError('Category title should be at least 3.')
        return data




class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price",
                  "category", "category_name", "stock",
                  "image", "created_at"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
    
    def create(self, validated_data):
          product = Product(**validated_data)
          product.slug = slugify(product.name)
          product.save()
          return product






class PageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageContent
        fields = ["id", "page_name", "content"]






class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ["id", "name", "role", "bio", "image"]
        
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'name',
            'body',
        ]
        
    def create(self, validated_data):
        product_id = self.context['product_pk']    
        return Comment.objects.create(product_id=product_id, **validated_data)
        


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'birth_date']      
        read_only_fields = ['user']
