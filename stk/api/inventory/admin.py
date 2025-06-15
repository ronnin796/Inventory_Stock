from django.contrib import admin
from .models import Product, Category, SubCategory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_name', 'category', 'sub_category', 'quantity', 'sales', 'order_date')
    search_fields = ('product_name',)
    list_filter = ('category', 'sub_category')  # ✅ Filters in the sidebar

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
