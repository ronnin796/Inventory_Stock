from django.http import HttpResponse
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Category, SubCategory
from .forms import ExcelUploadForm
# Create your views here.
def index(request):
    """
    Render the index page.
    """
    return HttpResponse("Hello, world! This is the index page of the inventory API.")


def import_products(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['excel_file']
            try:
                df = pd.read_excel(file)
                imported = 0
                skipped = 0

                for _, row in df.iterrows():
                    category_obj, _ = Category.objects.get_or_create(name=row['Category'].strip().title())
                    subcat_obj, _ = SubCategory.objects.get_or_create(name=row['Sub-Category'].strip().title(), category=category_obj)

                    if Product.objects.filter(order_id=row['Order ID'], product_name=row['Product Name']).exists():
                        skipped += 1
                        continue

                    Product.objects.create(
                        order_id=row['Order ID'],
                        product_name=row['Product Name'],
                        category=category_obj,
                        sub_category=subcat_obj,
                        quantity=int(row['Quantity']),
                        sales=float(row['Sales']),
                        order_date=pd.to_datetime(row['Order Date']).date()
                    )
                    imported += 1

                messages.success(request, f'Successfully imported {imported} rows. Skipped {skipped} duplicates.')

            except Exception as e:
                messages.error(request, f'Import failed: {e}')
            return redirect('upload_products')
    else:
        form = ExcelUploadForm()

    return render(request, 'inventory/upload.html', {'form': form})

def list_products(request):
    """
    Display all uploaded products with filtering.
    """
    products = Product.objects.select_related('category', 'sub_category').all().order_by('-order_date')
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('sub_category')

    if category_id:
        products = products.filter(category_id=category_id)
        subcategories = subcategories.filter(category_id=category_id)
    if subcategory_id:
        products = products.filter(sub_category_id=subcategory_id)

    return render(request, 'inventory/items.html', {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
    })
