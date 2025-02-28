from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import TemplateView



from .models import Category, Product, PageContent, TeamMember, Customer
from .paginations import DefaultPagination
from .serializers import *




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




class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer    
    
    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return Comment.objects.filter(product_id=product_pk).all()

    
    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}
    
    
    def destroy(self, request, pk):
        Comment = get_object_or_404(Comment, pk=pk)
        Comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser]
    
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)



class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()
    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpadateCartItemSerializer
        return CartItemSerializer 
    
    def get_serializer_context(self):
        return {'cart_pk': self.kwargs['cart_pk']}



class CartViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    serializer_class = CartSerializer 
    queryset = Cart.objects.prefetch_related('items__product').all()
    
    

class AboutView(TemplateView):
    template_name = "store/about.html"

class TermsView(TemplateView):
    template_name = "store/terms.html"

