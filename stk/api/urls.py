

from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from . views import index
urlpatterns = [
    path("", index, name="index"),  # Home page for the API
    path("inventory/", include("api.inventory.urls")),
    path("core/", include("api.core.urls")),

]
