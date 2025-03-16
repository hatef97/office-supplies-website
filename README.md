🏢 Office Supplies Website - API 📦

Welcome to the **Office Supplies Website** API! This project is a Django-based REST API for managing office supplies, customer orders, carts, and more. It leverages **Django Rest Framework (DRF)**, **Djoser for authentication**, and **Swagger for API documentation**.

🚀 Features

- 🔐 **User Authentication** (Registration, Login, Logout) using **Djoser**
- 🛍️ **Product Management** (Categories, Products)
- 🛒 **Shopping Cart** (Add, Update, Remove Items)
- 📦 **Order Processing** (Checkout, Order History)
- 📄 **Swagger API Documentation** (Integrated with drf-yasg)
- 📧 **Permissions for Admin & Customers**
- ✅ **Unit & Integration Tests** using Django's test framework

---

📌 Technologies Used

- **Backend:** Django, Django Rest Framework (DRF)
- **Authentication:** Djoser (Token-based authentication)
- **Database:** PostgreSQL / MySQL (Configurable)
- **API Documentation:** Swagger (drf-yasg)
- **Testing:** unittest and pytest

---

## 🛠 Installation & Setup

1. **Create & Activate a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Apply Database Migrations**
   ```sh
   python manage.py migrate
   ```

4. **Create a Superuser**
   ```sh
   python manage.py createsuperuser
   ```

5. **Run the Server**
   ```sh
   python manage.py runserver
   ```

---

## 🌐 API Documentation

- **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc:** [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

---

## 🚀 API Endpoints

| Method  | Endpoint                         | Description                        | Authentication |
|---------|----------------------------------|------------------------------------|---------------|
| `POST`  | `/auth/users/`                   | Register a new user               | ❌ No         |
| `POST`  | `/auth/token/login/`             | Get authentication token          | ❌ No         |
| `POST`  | `/auth/token/logout/`            | Logout user                       | ✅ Yes        |
| `GET`   | `/auth/users/me/`                | Get current user info             | ✅ Yes        |
| `GET`   | `/categories/`                   | List all categories               | ❌ No         |
| `POST`  | `/categories/`                   | Create a new category             | ✅ Admin      |
| `GET`   | `/products/`                     | List all products                 | ❌ No         |
| `POST`  | `/products/`                     | Create a new product              | ✅ Admin      |
| `GET`   | `/carts/`                        | Retrieve a cart                   | ✅ Yes        |
| `POST`  | `/carts/`                        | Create a new cart                 | ✅ Yes        |
| `POST`  | `/carts/{cart_id}/items/`        | Add item to cart                  | ✅ Yes        |
| `PATCH` | `/carts/{cart_id}/items/{id}/`   | Update item quantity in cart      | ✅ Yes        |
| `DELETE`| `/carts/{cart_id}/items/{id}/`   | Remove item from cart             | ✅ Yes        |
| `POST`  | `/orders/`                       | Place an order                    | ✅ Yes        |
| `GET`   | `/orders/`                       | Get order history                 | ✅ Yes        |
| `PATCH` | `/orders/{id}/`                  | Update order (Admin only)         | ✅ Admin      |
| `DELETE`| `/orders/{id}/`                  | Cancel order (Admin only)         | ✅ Admin      |

---

## ✅ Running Tests

Run the following command to execute tests:

```sh
python manage.py test
```

---

## 🐜 License

This project is licensed under the **BSD License**.

---

## 💌 Contact

For any issues or inquiries, reach out at:  
📎 **Email:** hatef.barin97@gmail.com


