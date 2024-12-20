# Library Management API

This project is a Django-based RESTful API for managing a library system. It includes functionality for managing books, user authentication, and borrowing and returning books.

## Features

### User Management
- **User Registration**: New users can create accounts
- **JWT Authentication**: Secure login system with access and refresh tokens
- **Logout Functionality**: Token invalidation for secure user logout

### Book Management
- **Book Catalog**: Comprehensive listing of all library books
- **Administrative Controls**: Restricted access for book addition, updates, and deletion
- **Detailed Views**: In-depth information for individual books

### Borrowing System
- **Book Borrowing**: Users can check out available books
- **Returns Processing**: Streamlined book return system
- **Borrowing History**: Personal borrowing record tracking

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/Library-Management-API.git
   cd library-management-api
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv .venv
   
   # On Unix/macOS
   source .venv/bin/activate
   
   # On Windows
   .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Administrator Account**
   ```bash
   python manage.py createsuperuser
   ```

6. **Launch Development Server**
   ```bash
   python manage.py runserver
   ```

## API Documentation

### Authentication Endpoints

| Endpoint | Method | Description | Access |
|----------|---------|-------------|---------|
| `/api/register/` | POST | Create new user account | Public |
| `/api/token/` | POST | Obtain JWT tokens | Public |
| `/api/logout/` | POST | Invalidate refresh token | Authenticated |


a)Register

    Endpoint  : api/register/
    Method    : POST     - Register User
    Data      : JSON     - { "name": "string", "password": "password" }
    
b)Login

    Endpoint  : api/login/
    Method    : POST     - User Login
    Data      : JSON     - { "name": "string", "password": "password" }
    
c)Logout

    Endpoint  : api/logout/
    Headers   - Key   :  Authorization
                Value :  Bearer "Your Access Token"

### Book Management Endpoints

| Endpoint | Method | Description | Access |
|----------|---------|-------------|---------|
| `/api/books/` | GET | List all books | Authenticated |
| `/api/books/create/` | POST | Add new book | Admin |
| `/api/books/<id>/` | GET | View book details | Authenticated |
| `/api/books/<id>/` | PUT | Update book | Admin |
| `/api/books/<id>/` | DELETE | Remove book | Admin |

### Borrowing Endpoints

| Endpoint | Method | Description | Access |
|----------|---------|-------------|---------|
| `/api/borrow/` | POST | Borrow a book | Authenticated |
| `/api/return/` | POST | Return a book | Authenticated |
| `/api/my-borrows/` | GET | View borrowing history | Authenticated |

a) Borrow

    Endpoint  : api/borrow/
    Method    : POST     
    Data      : JSON     - { "book_id" : id }
    Headers   - Key   :  Authorization
                Value :  Bearer "Your Access Token"

    Output -
    
    {
    "id": 1,
    "borrowed_at": "2024-12-20T07:04:51.039021Z",
    "returned_at": null,
    "user": 2,
    "book": 1
    }
b) My-Borrows

    Endpoint  : api/my-borrows/
    Method    : GET     
    Headers   - Key   :  Authorization
                Value :  Bearer "Your Access Token"

    Output -

    [
    {
        "id": 1,
        "borrowed_at": "2024-12-20T07:04:51.039021Z",
        "returned_at": null,
        "user": 2,
        "book": 1
    }
    ]
b) Return

    Endpoint  : api/return/
    Method    : POST     
    Data      : JSON     - { "borrow_id" : id }
    Headers   - Key   :  Authorization
                Value :  Bearer "Your Access Token"

    Output -

    {
    "id": 1,
    "borrowed_at": "2024-12-20T07:04:51.039021Z",
    "returned_at": "2024-12-20T07:16:29.167763Z",
    "user": 2,
    "book": 1
    }
