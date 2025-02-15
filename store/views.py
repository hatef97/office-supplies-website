from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404

from .models import Category, Product, PageContent, TeamMember
from .serializers import (
    CategorySerializer, ProductSerializer,
    PageContentSerializer, TeamMemberSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related("products")
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['price', 'category']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.select_related("category").all()  
        category_id = self.kwargs.get("category_pk")
        return queryset.filter(category_id=category_id) if category_id else queryset

    def create(self, request, *args, **kwargs):
        category_id = self.kwargs.get("category_pk")
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            request.data["category"] = category.id
        else:
            return Response({"error": "Category is required"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class PageContentViewSet(viewsets.ModelViewSet):
    queryset = PageContent.objects.all()
    serializer_class = PageContentSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
