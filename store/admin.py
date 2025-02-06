from django.contrib import admin
from .models import Product, Category, PageContent, TeamMember

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(PageContent)
admin.site.register(TeamMember)
