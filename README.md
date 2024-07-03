# **FarmApp**

![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)

## Overview

Farm App is a Django-based web application designed to facilitate interactions between farmers and suppliers. The application includes functionalities such as user authentication, profile management, product management, order processing, and an interactive analytics dashboard. The app is tailored to provide separate dashboards for farmers and suppliers, allowing for streamlined management of personal information, products, and orders.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Features

- User authentication (signup, login, password reset)
- Profile management (view and edit personal details, change profile picture)
- Separate dashboards for farmers and suppliers
- Product management (add, update, delete products)
- Order management (shopping cart, checkout, order history, order status tracking)
- Interactive analytics dashboard for suppliers

## Technologies Used
- [Python](https://www.python.org/): A high-level programming language used for developing the backend of the application.
- [Django](https://www.djangoproject.com/): A high-level Python web framework that enables rapid development of secure and maintainable websites.
- [SQLite](https://www.sqlite.org/): A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
- [Crispy Bootstrap](https://django-crispy-forms.readthedocs.io/en/latest/): A Django app that allows you to create beautiful forms using Bootstrap.
- [Pillow](https://python-pillow.org/): A Python Imaging Library that adds image processing capabilities to your Python interpreter.

## Installation

1. **Clone the repository**:
   ```bash
   https://github.com/MichaelSimiyu-Truth/Agro-connect.git
   ```
2  **Navigate to project directory**
   ```bash
   cd agro-connect-main
   ```
   
3. **Set up virtual environment**
  ```bash
   pip install virtualenv
  ```
   ```bash
   python -m virtualenv venv
   ```
   ```bash
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate
   ```

4. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```
   
5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```
       
   
6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```
        #Input username,email and password for the superuser
   
7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

  ## Usage
  
**Access the application:**
Open your web browser and go to http://127.0.0.1:8000/.

**Login or Signup:**

Create an account if you don't have one.
Login with your credentials.
Explore the features:

**Farmers**
Browse products.
Add products to the cart.
Place orders.

**Suppliers**
- Manage product listings.
- View order analytics.
- Access the interactive analytics dashboard.

**Admin**
- #visit  http://127.0.0.1:8000/admin for admin dashboard
- Manage users.
- Manage product categories.




