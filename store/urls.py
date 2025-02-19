from rest_framework_nested import routers

from django.urls import path

from . import views


router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'pages', views.PageContentViewSet, basename='pagecontent')
router.register(r'team', views.TeamMemberViewSet, basename='teammember')


product_router = routers.NestedDefaultRouter(router, r'categories', lookup='category')
product_router.register(r'products', views.ProductViewSet, basename='category-products')


products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('comments', views.CommentViewSet, basename='product-comments')


urlpatterns = router.urls + products_router.urls + [
    path('about/', views.AboutView.as_view(), name='about'),
    path('terms/', views.TermsView.as_view(), name='terms'),
]

