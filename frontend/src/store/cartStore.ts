import { create } from 'zustand';
import api from '../api/axios';
import { Cart } from '../types';

interface CartState {
  cart: Cart | null;
  isLoading: boolean;
  fetchCart: () => Promise<void>;
  addToCart: (productId: string, quantity: number) => Promise<void>;
  updateCartItem: (productId: string, quantity: number) => Promise<void>;
  removeFromCart: (productId: string) => Promise<void>;
}

export const useCartStore = create<CartState>((set) => ({
  cart: null,
  isLoading: false,

  fetchCart: async () => {
    try {
      set({ isLoading: true });
      const response = await api.get('/cart');
      set({ cart: response.data, isLoading: false });
    } catch (error) {
      set({ cart: null, isLoading: false });
    }
  },

  addToCart: async (productId, quantity) => {
    set({ isLoading: true });
    const response = await api.post('/cart/items', {
      product_id: productId,
      quantity,
    });
    set({ cart: response.data, isLoading: false });
  },

  updateCartItem: async (productId, quantity) => {
    set({ isLoading: true });
    const response = await api.put(`/cart/items/${productId}`, {
      quantity,
    });
    set({ cart: response.data, isLoading: false });
  },

  removeFromCart: async (productId) => {
    set({ isLoading: true });
    const response = await api.delete(`/cart/items/${productId}`);
    set({ cart: response.data, isLoading: false });
  },
}));
