# E-Commerce Platform - Full-Stack Implementation

A modern, production-ready e-commerce platform built with FastAPI, MongoDB, React, and TypeScript. This platform delivers a comprehensive shopping experience with features including user authentication, product search and filtering, shopping cart management, reviews and ratings, and a complete multi-step checkout flow with Stripe integration.

## 🚀 Project Overview

This is a complete, API-first e-commerce solution designed for scalability, security, and performance.

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Client Layer                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         React SPA (Vite + TypeScript)                   │   │
│  │  - Pages (Home, Products, Checkout, Admin)              │   │
│  │  - State Management (Zustand)                           │   │
│  │  - UI Components (shadcn/ui + Tailwind CSS)             │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS / REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       API Gateway Layer                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              FastAPI Application                         │   │
│  │  - CORS Middleware                                       │   │
│  │  - JWT Authentication Middleware                        │   │
│  │  - Request Validation (Pydantic)                        │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Routers    │  │   Services   │  │   Security   │          │
│  │              │  │              │  │              │          │
│  │ - Auth       │  │ - Product    │  │ - JWT Auth   │          │
│  │ - Products   │  │ - Cart       │  │ - Password   │          │
│  │ - Cart       │  │ - Order      │  │   Hashing    │          │
│  │ - Orders     │  │              │  │ - RBAC       │          │
│  │ - Admin      │  │              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Access Layer                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            Beanie ODM (Async MongoDB Driver)             │   │
│  │  - Document Models                                       │   │
│  │  - Query Builders                                        │   │
│  │  - Index Management                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Database Layer                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   MongoDB Database                       │   │
│  │  Collections:                                            │   │
│  │  - users (auth & profiles)                               │   │
│  │  - products (catalog)                                    │   │
│  │  - reviews (ratings & comments)                          │   │
│  │  - carts (shopping carts)                                │   │
│  │  - orders (transaction history)                          │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

                    External Services
┌────────────────────────────────────────────────────────────────┐
│                     Stripe Payment API                          │
│  - Payment Intent Creation                                      │
│  - Payment Confirmation                                         │
│  - Webhook Events                                               │
└────────────────────────────────────────────────────────────────┘
```

### Data Flow Architecture

#### 1. **User Authentication Flow**
```
User → Login Form → POST /auth/login → Validate Credentials
                                      ↓
                        Generate JWT Token → Set HttpOnly Cookie
                                      ↓
                        Return User Data → Update Auth State (Zustand)
                                      ↓
                        Redirect to Dashboard
```

#### 2. **Product Browsing Flow**
```
User → Browse Products → GET /products?filters → Query MongoDB
                                                ↓
                                    Apply Filters (category, price, search)
                                                ↓
                                    Return Paginated Results
                                                ↓
                                    Render Product Cards (React)
```

#### 3. **Shopping Cart Flow**
```
User → Add to Cart → POST /cart/items → Validate Stock
                                       ↓
                          Check User Authentication (JWT)
                                       ↓
                          Update Cart in MongoDB
                                       ↓
                          Return Updated Cart → Update Cart State (Zustand)
                                       ↓
                          Show Success Toast
```

#### 4. **Checkout & Payment Flow**
```
User → Checkout → GET /cart → Validate Cart Items
                             ↓
              Enter Shipping Address → Validate Address
                             ↓
              POST /orders/create-payment-intent → Stripe API
                             ↓
              Create Payment Intent → Return Client Secret
                             ↓
              Stripe Payment Element → User Enters Card
                             ↓
              Confirm Payment → Stripe Processes Payment
                             ↓
              POST /orders → Create Order Record
                             ↓
              Clear Cart → Update Stock → Redirect to Success Page
```

#### 5. **Admin Product Management Flow**
```
Admin → Admin Dashboard → POST /admin/products → Validate Admin Role
                                                ↓
                                    Validate Product Data (Pydantic)
                                                ↓
                                    Insert into MongoDB
                                                ↓
                                    Return Success → Refresh Product List
```

### Security Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     Security Layers                             │
├────────────────────────────────────────────────────────────────┤
│ 1. Transport Layer Security                                     │
│    - HTTPS (TLS/SSL)                                            │
│    - Secure Headers (CORS, CSP)                                 │
├────────────────────────────────────────────────────────────────┤
│ 2. Authentication & Authorization                               │
│    - JWT Tokens (HS256 Algorithm)                               │
│    - HttpOnly Cookies (XSS Protection)                          │
│    - Password Hashing (bcrypt)                                  │
│    - Role-Based Access Control (User/Admin)                     │
├────────────────────────────────────────────────────────────────┤
│ 3. Input Validation                                             │
│    - Pydantic Schema Validation                                 │
│    - Type Checking (TypeScript + Python)                        │
│    - Sanitization of User Input                                 │
├────────────────────────────────────────────────────────────────┤
│ 4. Data Protection                                              │
│    - Encrypted Passwords (never stored in plaintext)            │
│    - Secure Session Management                                  │
│    - Protected API Endpoints                                    │
└────────────────────────────────────────────────────────────────┘
```

### State Management Architecture

```
Frontend State (Zustand)
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────────────┐        ┌─────────────────────┐       │
│  │   Auth Store        │        │   Cart Store        │       │
│  │                     │        │                     │       │
│  │ - user: User | null │        │ - items: CartItem[] │       │
│  │ - isLoading: bool   │        │ - total: number     │       │
│  │ - login()           │        │ - addToCart()       │       │
│  │ - logout()          │        │ - removeFromCart()  │       │
│  │ - register()        │        │ - updateQuantity()  │       │
│  │ - fetchUser()       │        │ - fetchCart()       │       │
│  └─────────────────────┘        └─────────────────────┘       │
│           │                              │                     │
│           └──────────────┬───────────────┘                     │
│                          │                                     │
│                          ▼                                     │
│              ┌────────────────────┐                            │
│              │   API Axios Client │                            │
│              │  - Interceptors    │                            │
│              │  - Error Handling  │                            │
│              └────────────────────┘                            │
└────────────────────────────────────────────────────────────────┘
```

### Deployment Architecture

```
Production Environment
┌────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌──────────────────┐      ┌──────────────────┐               │
│  │   CDN (Static)   │      │   Web Server     │               │
│  │   - React Build  │      │   - FastAPI      │               │
│  │   - Images       │      │   - Uvicorn      │               │
│  │   - CSS/JS       │      │   - Gunicorn     │               │
│  └──────────────────┘      └──────────────────┘               │
│           │                          │                         │
│           └──────────┬───────────────┘                         │
│                      │                                         │
│                      ▼                                         │
│         ┌────────────────────────┐                             │
│         │   Load Balancer        │                             │
│         │   - SSL Termination    │                             │
│         │   - Health Checks      │                             │
│         └────────────────────────┘                             │
│                      │                                         │
│          ┌───────────┴───────────┐                             │
│          ▼                       ▼                             │
│  ┌──────────────┐        ┌──────────────┐                     │
│  │ MongoDB      │        │ Redis Cache  │                     │
│  │ - Replica Set│        │ - Sessions   │                     │
│  │ - Backups    │        │ - Rate Limit │                     │
│  └──────────────┘        └──────────────┘                     │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Tech Stack

**Backend:**
- **Python 3.11+** - Modern Python with async/await support
- **FastAPI** - High-performance async web framework
- **MongoDB** - NoSQL database for flexible schema design
- **Beanie** - Async ODM (Object Document Mapper) for type-safe database operations
- **Pydantic** - Data validation using Python type annotations
- **JWT Authentication** - Secure, token-based auth with httponly cookies
- **Stripe** - Payment processing integration

**Frontend:**
- **React 18** - Modern UI library with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Next-generation frontend tooling
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality, accessible component library
- **Zustand** - Lightweight state management
- **React Hook Form** - Performant form validation
- **Axios** - HTTP client with interceptors

## ✨ Features

### Core Features

#### 1. **User Authentication & Authorization**
- Secure registration and login with bcrypt password hashing
- JWT-based authentication using httponly cookies (XSS protection)
- Role-based access control (User vs Admin)
- Persistent sessions with refresh tokens
- Protected routes on both frontend and backend

#### 2. **Product Management**
- Browse products with pagination
- Advanced filtering by category
- Sort by price (ascending/descending)
- Full-text search across product names and descriptions
- Product detail pages with images, descriptions, and pricing
- Real-time stock tracking

#### 3. **Shopping Cart**
- Persistent cart stored in MongoDB (tied to user account)
- Add, remove, and update product quantities
- Real-time price calculations
- Cart state synchronized between backend and frontend
- Cart sidebar for quick access

#### 4. **Reviews & Ratings**
- Users can leave reviews on products they've viewed
- 5-star rating system
- Aggregate ratings automatically calculated
- Review count and average rating displayed on product cards
- Comment system for detailed feedback

#### 5. **Multi-Step Checkout**
- Shipping address collection and validation
- Stripe payment integration with Payment Intents API
- Secure payment element with card validation
- Order confirmation and success page
- Webhook handling for payment status updates

#### 6. **Order Management**
- Complete order history for users
- Order status tracking (pending, shipped, delivered)
- Detailed order breakdowns with line items
- Admin view of all orders across the platform

#### 7. **Admin Dashboard**
- Product CRUD operations (Create, Read, Update, Delete)
- Sales analytics and charts
- Order management and fulfillment
- User role management

### Security Features
- Password hashing with bcrypt
- JWT tokens stored in httponly cookies
- CORS configuration with credentials
- Protected API endpoints
- Admin-only routes
- Input validation and sanitization

## 📊 Database Schema

### Collections Overview

The platform uses MongoDB with the following collections:

#### **users**
Stores user account information and authentication data.

```
{
  _id: ObjectId
  email: string (unique, indexed)
  hashed_password: string
  first_name: string
  last_name: string
  is_admin: boolean (default: false)
  created_at: datetime
}
```

**Indexes:** `email` (unique)

**Relationships:**
- One-to-Many with `reviews` (user_id)
- One-to-Many with `orders` (user_id)
- One-to-One with `carts` (user_id)

---

#### **products**
Stores product catalog information.

```
{
  _id: ObjectId
  name: string (indexed for text search)
  description: string (indexed for text search)
  price: float
  imageUrl: string
  category: string (indexed)
  stock_quantity: integer
  avg_rating: float (default: 0)
  review_count: integer (default: 0)
  created_at: datetime
}
```

**Indexes:** 
- Text index on `name` and `description`
- Single index on `category`

**Relationships:**
- One-to-Many with `reviews` (product_id)
- Referenced in `cart` items and `order` items

---

#### **reviews**
Stores user reviews and ratings for products.

```
{
  _id: ObjectId
  product_id: ObjectId (indexed, references products)
  user_id: ObjectId (indexed, references users)
  rating: integer (1-5)
  comment: string
  created_at: datetime
}
```

**Indexes:** 
- `product_id` (for efficient product review queries)
- `user_id` (for user review history)

**Relationships:**
- Many-to-One with `products` (product_id)
- Many-to-One with `users` (user_id)

**Business Logic:** When a new review is added, the system automatically recalculates the product's `avg_rating` and `review_count`.

---

#### **carts**
Stores shopping cart state for each user.

```
{
  _id: ObjectId
  user_id: ObjectId (unique, indexed, references users)
  items: [
    {
      product_id: ObjectId (references products)
      quantity: integer
    }
  ]
  updated_at: datetime
}
```

**Indexes:** `user_id` (unique - one cart per user)

**Relationships:**
- One-to-One with `users` (user_id)
- References `products` in items array

**Notes:** Cart items are populated with full product details (name, price, image) when retrieved for display.

---

#### **orders**
Stores completed orders and transaction history.

```
{
  _id: ObjectId
  user_id: ObjectId (indexed, references users)
  items: [
    {
      product_id: ObjectId
      name: string
      price: float
      quantity: integer
    }
  ]
  total_amount: float
  shipping_address: {
    street: string
    city: string
    state: string
    zip_code: string
  }
  status: string ("pending" | "shipped" | "delivered")
  stripe_payment_intent_id: string
  created_at: datetime
}
```

**Indexes:** `user_id` (for user order history queries)

**Relationships:**
- Many-to-One with `users` (user_id)
- Denormalized product data in items array (snapshot at purchase time)

**Notes:** Order items store a snapshot of product data to preserve historical pricing and names.

---

## 🔌 API Endpoint Specification

Base URL: `http://localhost:8000/api/v1`

### Authentication Endpoints

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| POST | `/auth/register` | Create a new user account | Public |
| POST | `/auth/login` | Login and receive auth cookies | Public |
| POST | `/auth/logout` | Clear auth cookies and logout | User |
| GET | `/auth/me` | Get current authenticated user | User |

**Request/Response Examples:**

```json
// POST /auth/register
Request: {
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
Response: {
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_admin": false
}

// POST /auth/login
Request: {
  "username": "user@example.com",
  "password": "SecurePass123!"
}
Response: {
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
// Note: Tokens are set as httponly cookies
```

---

### Product Endpoints

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| GET | `/products` | List all products (with filters) | Public |
| GET | `/products/{id}` | Get single product details | Public |
| GET | `/products/{id}/reviews` | Get all reviews for a product | Public |
| POST | `/products/{id}/reviews` | Add a review to a product | User |

**Query Parameters for GET /products:**
- `skip` (int): Pagination offset (default: 0)
- `limit` (int): Number of items per page (default: 20)
- `category` (string): Filter by category
- `sort` (string): Sort order - `price_asc`, `price_desc`
- `q` (string): Search query (searches name and description)

**Example:**
```
GET /products?category=Electronics&sort=price_asc&q=laptop&skip=0&limit=10
```

---

### Cart Endpoints

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| GET | `/cart` | Get current user's cart | User |
| POST | `/cart/items` | Add item to cart | User |
| PUT | `/cart/items/{product_id}` | Update item quantity | User |
| DELETE | `/cart/items/{product_id}` | Remove item from cart | User |

**Request/Response Examples:**

```json
// POST /cart/items
Request: {
  "product_id": "507f1f77bcf86cd799439011",
  "quantity": 2
}

// GET /cart
Response: {
  "id": "507f191e810c19729de860ea",
  "user_id": "507f1f77bcf86cd799439011",
  "items": [
    {
      "product_id": "507f191e810c19729de860eb",
      "quantity": 2,
      "product": {
        "name": "Wireless Mouse",
        "price": 29.99,
        "imageUrl": "/images/mouse.jpg"
      }
    }
  ],
  "total": 59.98
}
```

---

### Order & Checkout Endpoints

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| POST | `/orders/create-payment-intent` | Create Stripe payment intent | User |
| POST | `/orders` | Create order after payment | User |
| GET | `/orders` | Get user's order history | User |
| POST | `/orders/stripe-webhook` | Stripe webhook handler | Public (verified) |

**Request/Response Examples:**

```json
// POST /orders/create-payment-intent
Response: {
  "clientSecret": "pi_3MtwBwLkdIwHu7ix28a3tqPa_secret_YrKJUKribcBjcG8HVhfZluoGH"
}

// POST /orders
Request: {
  "payment_intent_id": "pi_3MtwBwLkdIwHu7ix28a3tqPa",
  "shipping_address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001"
  }
}
```

---

### Admin Endpoints

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| POST | `/admin/products` | Create a new product | Admin |
| PUT | `/admin/products/{id}` | Update product details | Admin |
| DELETE | `/admin/products/{id}` | Delete a product | Admin |
| GET | `/admin/orders` | View all orders | Admin |

**Request Example:**

```json
// POST /admin/products
Request: {
  "name": "Wireless Keyboard",
  "description": "Mechanical RGB keyboard with Cherry MX switches",
  "price": 89.99,
  "imageUrl": "/images/keyboard.jpg",
  "category": "Electronics",
  "stock_quantity": 50
}
```

---

## 🛠️ Setup & Installation

### Prerequisites

- **Python 3.11+** installed
- **Node.js 18+** and npm installed
- **MongoDB** running (local or MongoDB Atlas)
- **Stripe Account** (for payment processing)

### Backend Setup

1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Create `.env` file in backend directory:**
   ```env
   MONGODB_URL=mongodb://localhost:27017/ecommerce
   JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
   ```

5. **Run the FastAPI server:**
   ```powershell
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Create `.env` file in frontend directory:**
   ```env
   VITE_API_URL=http://localhost:8000/api/v1
   VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
   ```

4. **Run the development server:**
   ```powershell
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

### Database Seeding

The backend automatically seeds the database with sample products on first startup if the products collection is empty. This includes:
- 15 sample products across multiple categories
- Realistic product names, descriptions, and pricing
- Sample images and stock quantities

### Creating an Admin User

To create an admin user, you'll need to manually update the database:

1. Register a normal user through the UI
2. Connect to MongoDB and update the user document:
   ```javascript
   db.users.updateOne(
     { email: "admin@example.com" },
     { $set: { is_admin: true } }
   )
   ```

Alternatively, modify the `seed_database()` function in `backend/app/db.py` to create an admin user on startup.

### Stripe Setup

1. Create a Stripe account at https://stripe.com
2. Get your test API keys from the Stripe Dashboard
3. Set up a webhook endpoint:
   - URL: `http://localhost:8000/api/v1/orders/stripe-webhook`
   - Events to listen for: `payment_intent.succeeded`, `payment_intent.payment_failed`
4. Copy the webhook signing secret to your `.env` file

For local development, use Stripe CLI to forward webhooks:
```powershell
stripe listen --forward-to localhost:8000/api/v1/orders/stripe-webhook
```

## 📁 Project Structure

```
ecommerce-platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration and environment variables
│   │   ├── db.py                   # Database initialization and seeding
│   │   ├── security.py             # Authentication and JWT utilities
│   │   ├── models/                 # Beanie document models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── review.py
│   │   │   ├── order.py
│   │   │   └── cart.py
│   │   ├── schemas/                # Pydantic schemas for API
│   │   │   ├── __init__.py
│   │   │   ├── user_schemas.py
│   │   │   ├── product_schemas.py
│   │   │   ├── review_schemas.py
│   │   │   ├── cart_schemas.py
│   │   │   └── order_schemas.py
│   │   ├── services/               # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── product_service.py
│   │   │   ├── cart_service.py
│   │   │   └── order_service.py
│   │   └── routers/                # API route handlers
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── products.py
│   │       ├── cart.py
│   │       ├── orders.py
│   │       └── admin.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── axios.ts           # Axios instance configuration
│   │   ├── components/
│   │   │   ├── ui/                # shadcn/ui components
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── form.tsx
│   │   │   │   ├── sheet.tsx
│   │   │   │   ├── table.tsx
│   │   │   │   └── ...
│   │   │   └── core/              # Application components
│   │   │       ├── Header.tsx
│   │   │       ├── Footer.tsx
│   │   │       ├── ProductCard.tsx
│   │   │       ├── StarRating.tsx
│   │   │       ├── CartSidebar.tsx
│   │   │       ├── ProtectedRoute.tsx
│   │   │       └── AdminRoute.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useCart.ts
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── ProductListPage.tsx
│   │   │   ├── ProductDetailPage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── OrderHistoryPage.tsx
│   │   │   ├── OrderSuccessPage.tsx
│   │   │   ├── Checkout/
│   │   │   │   ├── CheckoutPage.tsx
│   │   │   │   ├── ShippingForm.tsx
│   │   │   │   └── PaymentForm.tsx
│   │   │   └── Admin/
│   │   │       ├── AdminDashboard.tsx
│   │   │       ├── AdminProductList.tsx
│   │   │       └── AdminProductForm.tsx
│   │   ├── store/
│   │   │   ├── authStore.ts       # Zustand auth state
│   │   │   └── cartStore.ts       # Zustand cart state
│   │   ├── types/
│   │   │   └── index.ts           # TypeScript type definitions
│   │   ├── lib/
│   │   │   └── utils.ts           # Utility functions
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── .env
│
└── README.md
```

## 🚦 Development Workflow

### Running Tests
```powershell
# Backend tests (add pytest later)
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

### Building for Production

**Backend:**
```powershell
# Set production environment variables
# Deploy to a service like Railway, Render, or AWS
```

**Frontend:**
```powershell
cd frontend
npm run build
# Output will be in dist/ directory
```

## 🔐 Security Best Practices

1. **Environment Variables**: Never commit `.env` files. Use `.env.example` as templates.
2. **JWT Secrets**: Use strong, random secrets in production (min 32 characters).
3. **HTTPS**: Always use HTTPS in production for secure cookie transmission.
4. **CORS**: Restrict CORS origins to your production domain.
5. **Rate Limiting**: Implement rate limiting for API endpoints (add middleware).
6. **Input Validation**: All inputs are validated using Pydantic schemas.
7. **SQL Injection**: MongoDB with Beanie provides protection against injection attacks.

## 🎨 UI/UX Design Philosophy

The frontend is built with a focus on:
- **Clean, Modern Aesthetics**: Using Tailwind CSS and shadcn/ui for a polished look
- **Accessibility**: All components are keyboard navigable and screen-reader friendly
- **Responsive Design**: Mobile-first approach with breakpoints for all screen sizes
- **Performance**: Code splitting, lazy loading, and optimized re-renders
- **User Feedback**: Toast notifications, loading states, and error handling
- **Intuitive Navigation**: Clear hierarchy and easy-to-find actions

## 📈 Future Enhancements

- **Wishlist Feature**: Allow users to save products for later
- **Product Recommendations**: ML-based product suggestions
- **Email Notifications**: Order confirmations and shipping updates
- **Advanced Search**: Faceted search with multiple filters
- **Inventory Management**: Real-time stock updates and low-stock alerts
- **Discount Codes**: Coupon system for promotional campaigns
- **Multi-currency Support**: International pricing
- **Social Login**: OAuth integration (Google, Facebook)
- **Product Variants**: Size, color, and other options
- **Real-time Chat**: Customer support integration

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

This is a demonstration project. For a production deployment, consider:
- Adding comprehensive test coverage
- Implementing CI/CD pipelines
- Setting up monitoring and logging
- Adding caching layers (Redis)
- Implementing CDN for static assets
- Database backups and disaster recovery

---

**Built with ❤️ using FastAPI, MongoDB, React, and TypeScript**
