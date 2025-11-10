# PROMPT 1 
```
"
**Build Your Own.....!!**

**Task:**
Create an E-Commerce Website that enables users to explore products, view product details, and manage a shopping cart.
The site should have a clean and responsive UI, a lightweight backend to handle data operations, and basic state management for cart functionality.

**Artifacts to Deliver:**
1.  Technical architecture documentation
2.  Code base
3.  Prompts used for generating tech documentation and code base
"

Based on the above requirements and artifacts to deliver, generate a prompt to claude 4.5 that will inturn help me generate an end-to-end Amazon clone. 

I want it to use Python and FastAPI for the Backend; React and Typescript + whatever is needed for the frontend; and MongoDB for the Database.

It is imperative that I keep the number of prompts to a minimum, and therefore for this prompt to contain the entire picture.
```

# PROMPT 2 

```
MASTER INSTRUCTION: Generate a Complete, Full-Stack E-Commerce Platform

Objective:
Your task is to generate a complete, end-to-end, production-ready E-Commerce platform with functionality rivaling a core "Amazon" experience. This includes user authentication, a persistent shopping cart, product search and filtering, reviews and ratings, and a complete multi-step checkout flow with a mock payment integration.

The project will be built on a modern stack: Python/FastAPI for the backend, MongoDB for the database, and a unique, clean, high-performance UI using React, TypeScript, Tailwind CSS, and shadcn/ui components.

You must generate all artifacts, including comprehensive documentation first, followed by the complete, multi-file codebase for both the backend and frontend.

Core Philosophy & Design

API-First: The backend is a stateless, token-based JSON API.

Secure by Default: Implement JWT authentication with httponly cookies, password hashing, and protected routes.

Scalable Database: Use MongoDB with beanie (an async ODM) for efficient and type-safe data handling.

Modern UI/UX: The frontend must be fast, responsive, and aesthetically unique, using shadcn/ui components. It should NOT look like Amazon, but it must have its functional depth.

State Management: Use Zustand for simple, powerful global state management on the frontend (user auth, shopping cart).

Tech Stack

Backend: Python 3.11+, FastAPI, beanie (ODM for Motor/MongoDB), passlib[bcrypt] (hashing), python-jose[cryptography] (JWT), pydantic-settings.

Database: MongoDB.

Frontend: React 18, TypeScript, Vite, react-router-dom, axios, tailwindcss, shadcn/ui, lucide-react, Zustand, react-hook-form.

ARTIFACT 1: Technical Architecture & Documentation (README.md)

Generate a README.md file that explains the entire project. This file MUST include:

Project Overview: A brief description of the tech stack and purpose.

Features: A detailed list of all implemented features (Auth, Search, Cart, Checkout, etc.).

Database Schema:

A high-level explanation of the MongoDB collections.

Collections: users, products, reviews, orders, carts.

Detail the key fields and relationships for each collection (e.g., Review has a product_id and user_id).

API Endpoint Specification:

A complete table of all API endpoints, grouped by resource (e.g., Auth, Products, Cart, Orders, Admin).

For each endpoint, specify the:

HTTP Method (GET, POST, etc.)

Path (/api/v1/...)

Description

Required Auth (Public, User, Admin)

Setup & Installation: Step-by-step guide to run the backend and frontend.

ARTIFACT 2: Complete Backend Codebase (FastAPI)

Generate the complete, multi-file backend. Use beanie as the ODM for all database models.

backend/requirements.txt

(List all dependencies: fastapi, uvicorn[standard], beanie, motor, pydantic, pydantic-settings, passlib[bcrypt], python-jose[cryptography], stripe (for payment intent), email-validator)

backend/app/config.py

(Pydantic BaseSettings class to load env variables: MONGODB_URL, JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, STRIPE_SECRET_KEY)

backend/app/db.py

(Database initialization logic.

init_db() async function to be called on startup.

init_beanie with all document models (User, Product, Review, Order, Cart).

A get_db dependency.

Includes seed_database() function to populate products with 10-15 sample items if the collection is empty.)

backend/app/models/ (Data Models)

backend/app/models/user.py

(Beanie Document for User.

Fields: email (Pydantic EmailStr, unique=True), hashed_password, first_name, last_name, is_admin (bool, default False), created_at.

settings.name = "users")

backend/app/models/product.py

(Beanie Document for Product.

Fields: name, description, price (float), imageUrl, category (str, indexed), stock_quantity (int), avg_rating (float, default 0), review_count (int, default 0).

settings.name = "products"

indexes = [IndexModel("name", "description")] for text search.)

backend/app/models/review.py

(Beanie Document for Review.

Fields: product_id (Indexed(PydanticObjectId)), user_id (Indexed(PydanticObjectId)), rating (int, 1-5), comment (str), created_at.

settings.name = "reviews")

backend/app/models/order.py

(Pydantic models (not documents, as Order is complex).

OrderItem (Pydantic BaseModel): product_id, name, price, quantity.

ShippingAddress (Pydantic BaseModel): street, city, state, zip_code.

Beanie Document for Order:

Fields: user_id (Indexed(PydanticObjectId)), items (List[OrderItem]), total_amount (float), shipping_address (ShippingAddress), status (str, e.g., "pending", "shipped", "delivered"), stripe_payment_intent_id (str), created_at.

settings.name = "orders")

backend/app/models/cart.py

(Pydantic CartItem (BaseModel) and Beanie Cart Document.

CartItem: product_id, quantity.

Document for Cart:

Fields: user_id (Indexed(PydanticObjectId), unique=True), items (List[CartItem]), updated_at.

settings.name = "carts")

backend/app/schemas/ (API Schemas)

backend/app/schemas/user_schemas.py

(UserCreate, UserPublic, UserLogin, TokenData)

backend/app/schemas/product_schemas.py

(ProductCreate, ProductUpdate, ProductPublic)

backend/app/schemas/review_schemas.py

(ReviewCreate, ReviewPublic)

backend/app/schemas/cart_schemas.py

(CartItemCreate, CartPublic - which resolves product details)

backend/app/schemas/order_schemas.py

(OrderCreate (from cart), OrderPublic, CheckoutRequest)

backend/app/security.py

(All auth logic.

hash_password, verify_password.

create_access_token, create_refresh_token.

set_auth_cookies(response, access_token, refresh_token): Sets httponly cookies.

get_token_data(token): Verifies JWT.

get_current_user dependency: Reads httponly access token cookie.

get_current_admin_user dependency: Depends on get_current_user and checks is_admin flag.)

backend/app/services/ (Business Logic)

backend/app/services/product_service.py

(Logic for products.

recalculate_product_rating(product_id): Fetches all reviews for a product, calculates the new average, and updates the Product document. This MUST be called after a new review is added.)

backend/app/services/cart_service.py

(Logic for carts.

get_user_cart(user_id): Gets cart, creates if not exists.

add_item_to_cart(user_id, item: CartItemCreate): Adds item or updates quantity.

remove_item_from_cart(user_id, product_id).

get_populated_cart(user_id): Gets cart and populates product details (name, price, image) for the frontend.)

backend/app/services/order_service.py

(Logic for orders.

create_payment_intent(user_id): Calculates total from user's cart, creates a Stripe PaymentIntent, returns client_secret.

create_order_from_cart(user_id, payment_intent_id, shipping_address): Atomically creates an Order from the Cart, then clears the Cart.

handle_stripe_webhook(payload, signature): Processes webhooks, (e.g., payment_intent.succeeded) and updates order status.

backend/app/routers/ (API Routers)

backend/app/routers/auth.py

(APIRouter for authentication.

POST /auth/register: (UserCreate) -> UserPublic

POST /auth/login: (OAuth2PasswordRequestForm) -> Token (in httponly cookies).

POST /auth/logout: Clears cookies.

GET /auth/me: (Requires auth) -> UserPublic)

backend/app/routers/products.py

(APIRouter for products and reviews.

GET /products: Public. Supports pagination (skip, limit), filtering (category), sorting (price_asc, price_desc), and search (q).

GET /products/{id}: Public.

GET /products/{id}/reviews: Public.

POST /products/{id}/reviews: (Requires auth). Creates a Review, then calls recalculate_product_rating.)

backend/app/routers/cart.py

(APIRouter for cart. Requires auth.

GET /cart: Gets the user's populated cart.

POST /cart/items: Adds an item to the cart.

DELETE /cart/items/{product_id}: Removes an item.

PUT /cart/items/{product_id}: Updates item quantity.)

backend/app/routers/orders.py

(APIRouter for checkout and orders. Requires auth.

POST /orders/create-payment-intent: Creates Stripe intent, returns client_secret.

POST /orders: Creates the order in the DB after successful payment confirmation on frontend.

GET /orders: Gets the current user's order history.

POST /orders/stripe-webhook: Public, but requires signature verification. Listens for Stripe events.)

backend/app/routers/admin.py

(APIRouter for admin. Requires admin auth.

prefix="/admin", dependencies=[Depends(get_current_admin_user)]

POST /admin/products: Create product.

PUT /admin/products/{id}: Update product.

DELETE /admin/products/{id}: Delete product.

GET /admin/orders: View all orders.)

backend/app/main.py

(Main FastAPI app.

Sets up CORS (allowing frontend origin http://localhost:5173 and credentials).

Includes all API routers.

on_startup event handler to call init_db() and seed_database().
)

ARTIFACT 3: Complete Frontend Codebase (React + TS)

Generate the complete, multi-file frontend.

frontend/package.json

(Dependencies: react, react-dom, react-router-dom, axios, zustand, react-hook-form, @hookform/resolvers, zod, @stripe/react-stripe-js, @stripe/stripe-js, lucide-react, shadcn-ui deps (tailwind-merge, clsx, etc.), recharts (for admin dashboard))
(DevDependencies: @vitejs/plugin-react, typescript, tailwindcss, autoprefixer, postcss)

frontend/vite.config.ts

(Standard Vite config. No proxy needed as we'll use a full URL for API calls.)

frontend/tailwind.config.js

(Standard shadcn/ui tailwind config.)

frontend/src/lib/utils.ts

(The cn utility function for shadcn/ui.)

frontend/src/api/

frontend/src/api/axios.ts

(Creates an axios instance.

baseURL: 'http://localhost:8000/api/v1'

withCredentials: true (CRITICAL for httponly cookies))

frontend/src/types/index.ts

(All TypeScript types: User, Product, Review, Cart, CartItem, Order, OrderItem, ShippingAddress)

frontend/src/store/ (Zustand Stores)

frontend/src/store/authStore.ts

(Zustand store for auth.

State: user: User | null, isLoading: boolean.

Actions: login(email, password), register(...), logout(), fetchUser().

fetchUser (called on app load) hits /auth/me to check for a valid cookie session.)

frontend/src/store/cartStore.ts

(Zustand store for cart.

State: cart: Cart | null, isLoading: boolean.

Actions: fetchCart(), addToCart(productId, quantity), removeFromCart(productId).

All actions call the backend API and then re-fetch the cart to sync state.)

frontend/src/hooks/

(useAuth.ts and useCart.ts hooks that just export the Zustand store selectors for easy use.)

frontend/src/components/ui/

(Generate the code for the core shadcn/ui components needed:

button.tsx

card.tsx

input.tsx

label.tsx

form.tsx (for react-hook-form integration)

sheet.tsx (for cart sidebar)

table.tsx (for admin/order history)

dropdown-menu.tsx (for user profile)

separator.tsx

toast.tsx & use-toast.ts & toaster.tsx)

frontend/src/components/core/

frontend/src/components/core/Header.tsx

(Site-wide navigation.

Logo/Brand (links to /).

Search Bar (as a component, SearchBar.tsx).

Links: "All Products".

Right side:

CartButton.tsx: Uses SheetTrigger to open CartSidebar.tsx. Shows item count from useCart().

User Auth:

If user: DropdownMenu with "Hello, {user.firstName}", "My Orders", "Admin" (if is_admin), "Logout".

If !user: Button (links to /login) and Button (links to /register).)

frontend/src/components/core/Footer.tsx

(Standard site footer.)

frontend/src/components/core/ProductCard.tsx

(Displays a Product in a Card. Shows image, name, price, and StarRating component.)

frontend/src/components/core/StarRating.tsx

(Displays 1-5 stars (filled/empty) based on a rating prop.)

frontend/src/components/core/ProtectedRoute.tsx

(Auth guard. Uses useAuth. If isLoading, show spinner. If !user, redirect to /login. If user, render Outlet.)

frontend/src/components/core/AdminRoute.tsx

(Admin guard. Uses useAuth. If !user or !user.is_admin, redirect to /. Else, render Outlet.)

frontend/src/pages/

frontend/src/App.tsx

(Main app component.

Wraps everything in BrowserRouter.

Renders Toaster.

Has a useEffect that calls authStore.fetchUser() on mount.

Defines all routes using Routes and Route.)

frontend/src/pages/HomePage.tsx

(Landing page. Shows a hero section and "Featured Products" grid.)

frontend/src/pages/ProductListPage.tsx

(Main product grid.

Fetches products from /products.

State for filters (category), sort (price_asc), search (q).

Re-fetches when state changes.

Renders a FiltersSidebar.tsx and the ProductCard grid.)

frontend/src/pages/ProductDetailPage.tsx

(Single product.

useParams to get id.

Fetches /products/{id}.

Displays image, name, description, price.

"Add to Cart" button.

Renders ReviewList.tsx (fetches /products/{id}/reviews).

Renders ReviewForm.tsx (posts to /products/{id}/reviews).)

frontend/src/pages/LoginPage.tsx

(Login form using react-hook-form, zod, and shadcn/ui Form components. Calls authStore.login().)

frontend/src/pages/RegisterPage.tsx

(Register form, similar to Login.)

frontend/src/pages/Checkout/ (Multi-Step Checkout)

frontend/src/pages/Checkout/CheckoutPage.tsx

(Main checkout component.

Loads Stripe (loadStripe).

Wraps children in Elements provider.

Fetches payment intent from /orders/create-payment-intent and gets clientSecret.

Renders ShippingForm.tsx and PaymentForm.tsx (which needs the clientSecret).)

frontend/src/pages/Checkout/ShippingForm.tsx

(Form for shipping address. On submit, saves to a checkout state.)

frontend/src/pages/Checkout/PaymentForm.tsx

(Uses Stripe's useStripe, useElements, and PaymentElement. On submit, calls stripe.confirmPayment(). On success, calls backend /orders to create the order, then navigates to OrderSuccessPage.tsx.)

frontend/src/pages/OrderSuccessPage.tsx

("Thank you for your order!" page.)

frontend/src/pages/OrderHistoryPage.tsx

(Protected Route. Fetches /orders and displays a Table of past orders.)

frontend/src/pages/Admin/ (Admin Section)

frontend/src/pages/Admin/AdminDashboard.tsx

(Admin Route. Shows summary stats and charts (Recharts) of sales.)

frontend/src/pages/Admin/AdminProductList.tsx

(Admin Route. Table of all products with Edit/Delete buttons.)

frontend/src/pages/Admin/AdminProductForm.tsx

(Admin Route. Form (Create/Edit) for a product. Can be used for both creating a new product and editing an existing one by checking for an id in the URL params.)
```