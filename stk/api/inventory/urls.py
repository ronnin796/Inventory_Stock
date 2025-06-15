

from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from .views import index, import_products , list_products

urlpatterns = [
    path('import/', import_products, name='import_products'),
    path('list/', list_products, name='list_products'),

]
