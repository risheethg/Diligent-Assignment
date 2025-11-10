// User types
export interface User {
  _id: string;
  email: string;
  full_name: string;
  is_admin: boolean;
}

// Product types
export interface Product {
  _id: string;
  name: string;
  description: string;
  price: number;
  image_url: string;
  category: string;
  stock_quantity: number;
  avg_rating: number;
  review_count: number;
  created_at: string;
}

// Review types
export interface Review {
  _id: string;
  product_id: string;
  user_id: string;
  rating: number;
  comment: string;
  created_at: string;
  user_email: string;
}

// Cart types
export interface ProductInCart {
  _id: string;
  name: string;
  price: number;
  image_url: string;
  stock_quantity: number;
}

export interface CartItem {
  product_id: string;
  quantity: number;
  product?: ProductInCart;
}

export interface Cart {
  _id: string;
  user_id: string;
  items: CartItem[];
  total: number;
}

// Order types
export interface ShippingAddress {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
}

export interface OrderItem {
  product_id: string;
  product_name: string;
  price: number;
  quantity: number;
}

export interface Order {
  _id: string;
  user_id: string;
  user_email: string;
  items: OrderItem[];
  total_amount: number;
  shipping_address: ShippingAddress;
  status: string;
  stripe_payment_intent_id: string;
  created_at: string;
}

// Form types
export interface LoginFormData {
  email: string;
  password: string;
}

export interface RegisterFormData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface ReviewFormData {
  rating: number;
  comment: string;
}
