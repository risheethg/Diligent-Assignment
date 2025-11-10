import { useCartStore } from '../store/cartStore';

export const useCart = () => {
  const { cart, isLoading, fetchCart, addToCart, updateCartItem, removeFromCart } = useCartStore();

  return {
    cart,
    isLoading,
    itemCount: cart?.items.reduce((sum, item) => sum + item.quantity, 0) || 0,
    fetchCart,
    addToCart,
    updateCartItem,
    removeFromCart,
  };
};
