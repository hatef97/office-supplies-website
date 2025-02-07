from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404

from .models import Category, Product, PageContent, TeamMember
from .serializers import (
    CategorySerializer, ProductSerializer,
    PageContentSerializer, TeamMemberSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['price', 'category']

    def get_queryset(self):
        category_id = self.kwargs.get("category_pk")  
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()

    def create(self, request, *args, **kwargs):
        category_id = self.kwargs.get("category_pk")
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            request.data["category"] = category.id  

        return super().create(request, *args, **kwargs)


class PageContentViewSet(viewsets.ModelViewSet):
    queryset = PageContent.objects.all()
    serializer_class = PageContentSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
