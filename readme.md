# Supermarket Backend

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

1. Clone the repository:
    ```bash
    git clone 
   
2. Create a virtual environment and activate it:
   
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

