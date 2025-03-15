from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from debug_toolbar.toolbar import debug_toolbar_urls



schema_view = get_schema_view(
    openapi.Info(
        title="Office Supplies Website",
        default_version='v1',
        description="API documentation for Django project",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="hatef.barin97@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('store/', include('store.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')), 
    # Swagger UI (HTML view)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # ReDoc (Alternative documentation)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Raw JSON/YAML schema
    re_path(r'^swagger\.(?P<format>json|yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
