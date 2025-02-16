from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import OrderingFilter, SearchFilter

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


from .models import Category, Product, PageContent, TeamMember
from .paginations import DefaultPagination
from .serializers import (
    CategorySerializer, ProductSerializer,
    PageContentSerializer, TeamMemberSerializer
)




class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]
    ordering_fields = ['name', 'price', 'stock']
    search_fields = ['name']
    pagination_class = DefaultPagination
    queryset = Product.objects.select_related("category")
    
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related('category'),
            pk=pk
        )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('products').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    

    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, pk):
        category = get_object_or_404(Category.objects.prefetch_related('products'),
                    pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'There is some products relating this category. Please remove them first.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class PageContentViewSet(ModelViewSet):
    queryset = PageContent.objects.all()
    serializer_class = PageContentSerializer




class TeamMemberViewSet(ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
