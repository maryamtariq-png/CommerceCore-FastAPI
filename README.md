# CommerceCore – FastAPI E-Commerce Backend API

**CommerceCore** is a backend API for an e-commerce platform built using **FastAPI** and **Python**.  
The project provides essential functionalities required for an online shopping system, including user authentication, product management, cart operations, order processing, and payment simulation.

The API follows a **modular and scalable architecture**, separating routers, models, schemas, and services to maintain clean and maintainable code. It uses **SQLAlchemy as the ORM** for database interactions and **JWT (JSON Web Tokens)** for secure authentication and authorization.

The system allows users to register and log in, browse products, add items to their cart, place orders, and simulate payments through a service layer. FastAPI’s automatic documentation also provides interactive API testing through **Swagger UI**, making it easy to explore and test endpoints.

This project demonstrates key backend development concepts such as:

- RESTful API design
- Authentication and authorization
- Database modeling
- Service-based architecture
- Secure password handling

It serves as a **solid foundation for building scalable web applications**.

---

# Features

### User Authentication
- JWT-based authentication
- Secure password hashing

### User Management
- User registration
- Login system

### Product Management
- Create products
- View products
- Update products
- Delete products

### Cart System
- Add items to cart
- Remove items from cart
- View cart items

### Order Management
- Place orders
- Track order history

### Payment Simulation
- Stripe payment service integration (simulation)

---

# Tech Stack

- **Framework:** FastAPI  
- **Language:** Python  
- **Database:** SQLite (via aiosqlite)  
- **ORM:** SQLAlchemy 2.0 (Async)  
- **Security:** Jose (JWT), Passlib (Bcrypt)  
- **Payments:** Stripe Python SDK  
- **Validation:** Pydantic v2  

---

## How to Run
1. Clone the repo:
- git clone https://github.com/maryamtariq-png/CommerceCore-FastAPI.git
- cd CommerceCore-FastAPI

2. Install dependencies: 
- `pip install -r requirements.txt`

3. Create a virtual environment:
- python -m venv venv
- **Activate the environment**:
- **Windows**:
- venv\Scripts\activate
- **macOS / Linux**:
- source venv/bin/activate

4. Run the server: `uvicorn main:app --reload`
- Open in browser
- Swagger UI (interactive API docs):
- http://127.0.0.1:8000/docs
- ReDoc docs:
- http://127.0.0.1:8000/redoc

