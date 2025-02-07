from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'pages', views.PageContentViewSet, basename='pagecontent')
router.register(r'team', views.TeamMemberViewSet, basename='teammember')


product_router = routers.NestedDefaultRouter(router, r'categories', lookup='category')
product_router.register(r'products', views.ProductViewSet, basename='category-products')

urlpatterns = router.urls + product_router.urls 