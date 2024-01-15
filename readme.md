# Django Shop Project Readme

## Table of Contents

1. [Project Description](#project-description)
2. [Project Structure](#project-structure)
3. [Functionality](#functionality)
4. [Installation](#installation)
5. [Usage](#usage)


## Project Description

The project is a django restapi application with a basic web-front, all together providing a simple online shop with the following main components:
- **Products**: Users can view a list of available products, including their descriptions, prices, and images.
- **Shopping Cart**: Users can add products to their cart, adjust the quantity of items, and remove items from the cart.
- **User Authentication**: Users can register and log in to the system to save their cart and proceed to checkout.
- **Checkout**: Registered users can finalize their orders and view the total price of the items in their cart.

## Project Structure

The project consists of the following main components:

- **Models** (my_app/models.py): These define the data structures for the application. The models include `Category`, `Product`, `Order`, and `OrderDetails`.

- **Views** (my_app/views.py): These handle user requests and responses. The views include user registration, product CRUD operations, and cart checkout.

- **URLs** (my{app/urls.py}): The URL patterns are defined to route requests to the appropriate views.

- **HTML Templates** (front/): The project includes HTML templates for the main shop page and the login page.

- **JavaScript Files** (front/js/): JavaScript files are used for dynamic functionality on the web pages, such as adding items to the cart and performing user authentication.

## Functionality

The main functionality of the project includes:
- User registration and login.
- Displaying a list of products.
- Adding products to a shopping cart.
- Modifying the quantity of items in the cart.
- Removing items from the cart.
- Checking out and placing an order with the total price.

## Installation

To run this Django project, follow these steps:

1. Clone the repository:
    ```bash
    git clone git remote add origin https://github.com/MosheL2680/super_django.git
   
2. Create a virtual environment and activate it:
    ```bash 
    py -m virtualenv venv
    venv\Scripts\Activate
   
3. Install the project dependencies:
    ```bash
    pip install -r requirements.txt
   
4. Apply database migrations:
    ```bash
    py manage.py makemigrations
    py manage.py migrate
   
5. Create a superuser for administrative access to the admin panel:
    ```bash
    py manage.py createsuperuser
   
6. Start the development server:
    ```bash
    py manage.py runserver

The project should now be accessible at `http://127.0.0.1:8000/`.

## Usage

1. Run the main shop page (index.html) with the "default browser" extensin.
2. Register a new user account or log in to an existing account.
3. Add products to your shopping cart by adjusting the quantity and clicking "Add to cart."
4. Review the items in your cart and their total price.
5. Click the "Checkout" button to place an order.

