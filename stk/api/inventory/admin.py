from django.contrib import admin
from .models import  Category, SubCategory , MasterProduct, Product_sales
@admin.register(MasterProduct)
class MasterProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'sub_category', 'current_stock', 'reorder_threshold')
    search_fields = ('name',)
    list_filter = ('category', 'sub_category')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

@admin.register(Product_sales)
class ProductSalesAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product', 'quantity', 'sales', 'order_date')  # ✅ All fields explicitly listed
    search_fields = ('order_id', 'product__name')
    list_filter = ('order_date','product__category', 'product__sub_category')

