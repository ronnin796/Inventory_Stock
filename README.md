# Minimal Stock Inventory System

A minimal Django-based inventory management system for uploading, categorizing, and viewing products from Excel files.

## Features

- Upload products using Excel files (`.xls`, `.xlsx`)
- Organize products by Category and Sub-Category
- View and filter products by Category and Sub-Category
- Simple and user-friendly interface

## Setup

1. **Clone the repository**
    ```bash
    git clone https://github.com/ronnin796/Inventory_Stock.git
    cd Inventory_stock
    ```

2. **Create and activate a virtual environment**
    ```bash
    #Use anaconda or pipenv shell
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser (optional, for admin access)**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**
    ```bash
    python manage.py runserver
    ```

7. **Access the application**
    - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage

- **Upload Products:** Click "Upload Products" on the home page to upload an Excel file.
- **View Products:** Click "View Products" to see and filter all uploaded products.

## Project Structure

- `stk/api/inventory/models.py` — Django models for Category, SubCategory, and Product
- `stk/api/inventory/views.py` — Views for uploading and listing products
- `stk/api/inventory/templates/inventory/` — HTML templates for the app

## Requirements

See `requirements.txt` for all Python package dependencies.

## License

This project is licensed under the MIT License.