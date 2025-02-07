from rest_framework import serializers

from .models import Category, Product, PageContent, TeamMember


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


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "description", "products"]


class PageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageContent
        fields = ["id", "page_name", "content"]


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ["id", "name", "role", "bio", "image"]
