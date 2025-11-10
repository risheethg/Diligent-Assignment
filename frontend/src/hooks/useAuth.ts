import { useAuthStore } from '../store/authStore';

export const useAuth = () => {
  const { user, isLoading, login, register, logout, fetchUser } = useAuthStore();

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    isAdmin: user?.is_admin || false,
    login,
    register,
    logout,
    fetchUser,
  };
};
