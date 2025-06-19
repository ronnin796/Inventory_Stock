from django.http import HttpResponse
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MasterProduct, Category, SubCategory, Product_sales
from .forms import ExcelUploadForm

def index(request):
    return HttpResponse("Hello, world! This is the index page of the inventory API.")

def import_products(request):
    """
    Import product sales data from Excel and auto-create categories, subcategories,
    and master products if they don't exist.
    """
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['excel_file']
            try:
                df = pd.read_excel(file)
                imported = 0
                skipped = 0

                for _, row in df.iterrows():
                    # Get or create category and subcategory
                    category_obj, _ = Category.objects.get_or_create(name=row['Category'].strip().title())
                    subcat_obj, _ = SubCategory.objects.get_or_create(
                        name=row['Sub-Category'].strip().title(),
                        category=category_obj
                    )

                    # Get or create master product
                    product_name = row['Product Name'].strip()
                    master_product, _ = MasterProduct.objects.get_or_create(
                        name=product_name,
                        defaults={
                            'category': category_obj,
                            'sub_category': subcat_obj,
                            'current_stock': 20,
                            'reorder_threshold': 10,
                        }
                    )

                    # Check for duplicate sale entry (based on order ID and product)
                    if Product_sales.objects.filter(order_id=row['Order ID'], product=master_product).exists():
                        skipped += 1
                        continue

                    # Save the sale record
                    Product_sales.objects.create(
                        order_id=row['Order ID'],
                        product=master_product,
                        quantity=int(row['Quantity']),
                        sales=float(row['Sales']),
                        order_date=pd.to_datetime(row['Order Date']).date()
                    )

                    # Decrease stock
                

                    imported += 1

                messages.success(request, f'Successfully imported {imported} rows. Skipped {skipped} duplicates.')
            except Exception as e:
                messages.error(request, f'Import failed: {e}')
            return redirect('list_products')
    else:
        form = ExcelUploadForm()

    return render(request, 'inventory/upload.html', {'form': form})


def list_products(request):
    """
    Display sales data with filtering by category and subcategory.
    """
    sales = Product_sales.objects.select_related('product__category', 'product__sub_category').all().order_by('-order_date')
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('sub_category')

    if category_id:
        sales = sales.filter(product__category_id=category_id)
        subcategories = subcategories.filter(category_id=category_id)
    if subcategory_id:
        sales = sales.filter(product__sub_category_id=subcategory_id)

    return render(request, 'inventory/items.html', {
        'sales': sales,
        'categories': categories,
        'subcategories': subcategories,
    })
