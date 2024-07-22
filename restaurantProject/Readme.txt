# Restaurant_management_system
This project is a Restaurant Management System built with Django. It provides functionality for managing menu items, orders, and Users, along with user authentication and role-based access control.

## Features

- User authentication (Sign up, Log in, Log out)
- Role-based access control (Waiter, Viewer, Owner, Chef)
- Menu management (Add, Update, Delete menu items)
- Order management (Create, View, Update, Delete orders)
- Generate and download order history as CSV
- RESTful API for managing menu items, orders, and customers


## Technologies Used

- Django
- Django REST Framework
- PostgreSQL
- HTML, CSS
- JavaScript (for alerts in save and add another)


## Prerequisites

- Python 3.x
- PostgreSQL
- Django


## Installation


1. Create and activate a virtual environment:

    ```
    python -m venv venv
    venv\Scripts\activate
    ```

2. Install the dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Set up the PostgreSQL database:

    - Create a database named rest_DB
    - Update the `DATABASES` setting in `settings.py` with your database credentials.

4. Apply the migrations:

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Make the groups:

    ```
    python manage.py create_groups
    ```

6. Create a superuser:

    ```
    python manage.py createsuperuser
    ```

7. Run the development server:

    ```
    python manage.py runserver
    ```

8. Access the application:

    - Visit `http://127.0.0.1:8000` to view the application.
    - Visit `http://127.0.0.1:8000/admin` to access the Django admin interface.

## Project Structure

```
RESTAURANTPROJECT/
├── restApp/
│   ├── management/
│   │    └── commands/
│   │         ├── __init__.py
│   │         └── create_user_groups.py
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── restaurantProject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── views.py
│   └── asgi.py
├── static/
│   ├── css/
│   │    └── styles.css
│   ├── images/
│   │    └── loginBack.jpg
├── templates/
│   ├── account/
│   │    ├── sucess.html
│   │    └── signup.html
│   ├── registration/
│   │    ├── login.html
│   ├── restaurantApp/
│   │    ├── accept_order.html
│   │    ├── add_to_menu.html
│   │    └──base.html
│   │    └── create_order.html
│   │    └── login.html
│   │    └── myorders.html
│   │    └── order_detail.html
│   │    └── order_list.html
│   │    └── update_order_status.html
│   │    └── update_order.html
├── manage.py
└── requirements.txt
```

## User Roles

- Chef: Can view customers, can update the status of Item, menu items and orders and manage menu items
- User Service: Can view menu items and my orders and manage order items
- Owner/Manager: Can view and manage Orders, menu items .
- Waiter: Can view customers, menu items and orders and manage orders


## Authentication

- Users can sign up and log in.
- Upon signing up, users are automatically added to the selected group (role).


## Menu Management

- Add, update, and delete menu items.
- View a list of all menu items.


## Order Management

- Create new orders.
- View, update, and delete existing orders.
- Update the status of order item.
- Download order history as a CSV file.


## Customer Management

- Add ,update and delete the items in the order.
- View a list of menu items.


## REST API

The project also provides a RESTful API for managing menu items, orders, and order details. The API is secured with token-based authentication.


## Endpoints

### Menu Items:

- GET /api/menuitems/ - List all menu items
- POST /api/menuitems/ - Create a new menu item
- GET /api/menuitems/<id>/ - Retrieve a menu item
- PUT /api/menuitems/<id>/ - Update a menu item
- DELETE /api/menuitems/<id>/ - Delete a menu item

### Orders:

- GET /api/orderitems/ - List all orders
- POST /api/orderitems/ - Create a new order
- GET /api/orderitems/<id>/ - Retrieve an order
- PUT /api/orderitems/<id>/ - Update an order
- DELETE /api/orderitems/<id>/ - Delete an order


## Authentication

To access the API, you need to obtain an authentication token. Use the following endpoint to obtain a token:

- POST /api-token-auth/ - Obtain an authentication token