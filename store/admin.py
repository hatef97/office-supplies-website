from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from . import models




class StockFilter(admin.SimpleListFilter):
    LESS_THAN_3 = '<3'
    BETWEEN_3_and_10 = '3<=10'
    MORE_THAN_10 = '>10'
    title = 'Critical Stock Status'
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        return [
            (StockFilter.LESS_THAN_3, 'High'),
            (StockFilter.BETWEEN_3_and_10, 'Medium'),
            (StockFilter.MORE_THAN_10, 'OK'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == StockFilter.LESS_THAN_3:
            return queryset.filter(stock__lt=3)
        if self.value() == StockFilter.BETWEEN_3_and_10:
            return queryset.filter(stock__range=(3, 10))
        if self.value() == StockFilter.MORE_THAN_10:
            return queryset.filter(stock__gt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'category', 'stock', 'image', 'created_at']
    list_per_page = 10
    list_editable = ['price']
    list_select_related = ['category']
    list_filter = ['created_at', StockFilter]
    actions = ['clear_stock']
    search_fields = ['name', ]


    def get_queryset(self, request):
        return super().get_queryset(request) \
                .prefetch_related('comments') \
                .annotate(
                    comments_count=Count('comments'),
                )

    def stock_status(self, product):
        if product.stock < 10:
            return 'Low'
        if product.stock > 50:
            return 'High'
        return 'Medium'
    
    @admin.display(description='# comments', ordering='comments_count')
    def num_of_comments(self, product):
        url = (
            reverse('admin:store_comment_changelist') 
            + '?'
            + urlencode({
                'product__id': product.id,
            })
        )
        return format_html('<a href="{}">{}</a>', url, product.comments_count)
        
    
    @admin.display(ordering='category__name')
    def product_category(self, product):
        return product.category.name

    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} of products inventories cleared to zero.',
            messages.ERROR,
        )



@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'status', ]
    list_editable = ['status']
    list_per_page = 10
    autocomplete_fields = ['product', ]    
    
    
    
    



admin.site.register(models.Category)
admin.site.register(models.PageContent)
admin.site.register(models.TeamMember)
