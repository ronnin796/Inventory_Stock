from datetime import timedelta
from statsmodels.tsa.arima.model import ARIMA
from django.shortcuts import render
from api.inventory.models import MasterProduct, Product_sales, Category, SubCategory
import pandas as pd

def forecast_trend_view(request):
    selected_product = None
    forecast_data = None
    forecast_labels = []
    actual_sales = []
    alert_message = ""
    predicted_stock = None  # <-- Add this

    # Get filter parameters
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("sub_category")
    product_id = request.GET.get("product")

    # Get all categories
    categories = Category.objects.all()

    # Filter subcategories by category if selected
    if category_id:
        subcategories = SubCategory.objects.filter(category_id=category_id)
    else:
        subcategories = SubCategory.objects.all()

    # Filter products by subcategory or category if selected
    products = MasterProduct.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    if subcategory_id:
        products = products.filter(sub_category_id=subcategory_id)

    # Handle product selection and forecasting
    if product_id:
        try:
            selected_product = MasterProduct.objects.get(id=product_id)
            sales_qs = Product_sales.objects.filter(product=selected_product).order_by('order_date')

            if sales_qs.count() < 2:
                alert_message = "Not enough data to forecast."
            else:
                df = pd.DataFrame.from_records(
                    sales_qs.values('order_date', 'quantity')
                )

                df = df.sort_values('order_date').reset_index(drop=True)
                df['day'] = range(len(df))  # Synthetic index for time
                df = df.set_index('day')

                actual_sales = list(df['quantity'])

                if df['quantity'].sum() == 0:
                    alert_message = "Sales data contains only zeros. Unable to forecast."
                else:
                    model = ARIMA(df['quantity'], order=(1, 1, 1))
                    model_fit = model.fit()
                    forecast_result = model_fit.forecast(steps=7)

                    forecast_labels = [f"Day {i+1}" for i in range(len(df), len(df) + 7)]
                    forecast_data = list(forecast_result)

                    # Predicted stock after forecast period
                    total_predicted_sales = sum(forecast_data)
                    predicted_stock = selected_product.current_stock - total_predicted_sales

                    # Alert system
                    avg_predicted_sales = total_predicted_sales / len(forecast_data)
                    if predicted_stock <= selected_product.reorder_threshold:
                        alert_message = (
                            f"Restock soon! Forecasted average sales is {avg_predicted_sales:.2f}, "
                            f"stock will drop to {predicted_stock:.2f}"
                        )
        except MasterProduct.DoesNotExist:
            alert_message = "Invalid product selected."

    return render(request, "forecast/forecast_trend.html", {
        "categories": categories,
        "subcategories": subcategories,
        "products": products,
        "selected_product": selected_product,
        "forecast_data": forecast_data,
        "forecast_labels": forecast_labels,
        "actual_sales": actual_sales,
        "alert_message": alert_message,
        "predicted_stock": predicted_stock,  # <-- Pass to template
    })
