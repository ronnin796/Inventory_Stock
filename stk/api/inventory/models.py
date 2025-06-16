from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        unique_together = ('name', 'category')
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class MasterProduct(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category , on_delete=models.SET_NULL , null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    current_stock = models.IntegerField(default=100)
    reorder_threshold = models.IntegerField(default=10)
    class Meta:
        verbose_name_plural = "Master Products"
    def __str__(self):
        return self.name

class Product_sales(models.Model):
    order_id = models.CharField(max_length=50)
    product= models.ForeignKey(MasterProduct, on_delete=models.CASCADE, related_name='sales')
    quantity = models.IntegerField()
    sales = models.FloatField()
    order_date = models.DateField()

    class Meta:
        verbose_name_plural = "Products_Sales"
        ordering = ['-order_date']

    def __str__(self):
        return self.product.name
