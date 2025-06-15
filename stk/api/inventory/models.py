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


class Product(models.Model):
    order_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    sales = models.FloatField()
    order_date = models.DateField()

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.product_name
