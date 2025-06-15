from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    """
    Render the index page.
    """
    return HttpResponse("Hello, world! This is the index page of the inventory API.")