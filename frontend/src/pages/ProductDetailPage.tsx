import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api/axios";
import { Product, Review } from "../types";
import { useCartStore } from "../store/cartStore";
import { useAuthStore } from "../store/authStore";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { Input } from "../components/ui/input";

const ProductDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [product, setProduct] = useState<Product | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [rating, setRating] = useState(5);
  const [reviewComment, setReviewComment] = useState("");
  const { addToCart } = useCartStore();
  const { user } = useAuthStore();

  useEffect(() => {
    fetchProductDetails();
    fetchReviews();
  }, [id]);

  const fetchProductDetails = async () => {
    try {
      const response = await api.get(`/products/${id}`);
      setProduct(response.data);
    } catch (error) {
      console.error("Error fetching product:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchReviews = async () => {
    try {
      const response = await api.get(`/products/${id}/reviews`);
      setReviews(response.data);
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  };

  const handleAddToCart = async () => {
    if (!product) return;
    try {
      await addToCart(product._id, quantity);
      alert("Added to cart!");
    } catch (error) {
      console.error("Error adding to cart:", error);
      alert("Failed to add to cart. Please login.");
    }
  };

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) {
      alert("Please login to submit a review");
      navigate("/login");
      return;
    }
    try {
      await api.post(`/products/${id}/reviews`, {
        rating,
        comment: reviewComment,
      });
      setReviewComment("");
      setRating(5);
      fetchReviews();
      fetchProductDetails();
      alert("Review submitted successfully!");
    } catch (error) {
      console.error("Error submitting review:", error);
      alert("Failed to submit review");
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl">Product not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          {/* Product Image */}
          <div>
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full rounded-lg shadow-lg"
            />
          </div>

          {/* Product Info */}
          <div>
            <h1 className="text-4xl font-bold mb-4">{product.name}</h1>
            <p className="text-gray-600 mb-4">{product.category}</p>
            <div className="flex items-center mb-4">
              <div className="flex items-center text-yellow-500 text-xl">
                {"★".repeat(Math.round(product.avg_rating))}
                {"☆".repeat(5 - Math.round(product.avg_rating))}
              </div>
              <span className="ml-2 text-gray-600">
                {product.avg_rating.toFixed(1)} ({product.review_count} reviews)
              </span>
            </div>
            <p className="text-4xl font-bold text-blue-600 mb-6">
              ${product.price.toFixed(2)}
            </p>
            <p className="text-gray-700 mb-6">{product.description}</p>

            {product.stock_quantity > 0 ? (
              <>
                <div className="mb-6">
                  <label className="block text-sm font-medium mb-2">Quantity</label>
                  <Input
                    type="number"
                    min="1"
                    max={product.stock_quantity}
                    value={quantity}
                    onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
                    className="w-24"
                  />
                  <p className="text-sm text-gray-600 mt-2">
                    {product.stock_quantity} items available
                  </p>
                </div>
                <Button onClick={handleAddToCart} size="lg" className="w-full md:w-auto">
                  Add to Cart
                </Button>
              </>
            ) : (
              <div className="bg-red-100 text-red-700 p-4 rounded-lg">
                Out of Stock
              </div>
            )}
          </div>
        </div>

        {/* Reviews Section */}
        <div className="mb-12">
          <h2 className="text-3xl font-bold mb-6">Customer Reviews</h2>

          {/* Submit Review Form */}
          {user && (
            <Card className="mb-8">
              <CardContent className="pt-6">
                <h3 className="text-xl font-semibold mb-4">Write a Review</h3>
                <form onSubmit={handleSubmitReview}>
                  <div className="mb-4">
                    <label className="block text-sm font-medium mb-2">Rating</label>
                    <div className="flex gap-2">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          key={star}
                          type="button"
                          onClick={() => setRating(star)}
                          className={`text-3xl ${
                            star <= rating ? "text-yellow-500" : "text-gray-300"
                          }`}
                        >
                          ★
                        </button>
                      ))}
                    </div>
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium mb-2">Comment</label>
                    <textarea
                      className="w-full p-2 border border-gray-300 rounded-md"
                      rows={4}
                      value={reviewComment}
                      onChange={(e) => setReviewComment(e.target.value)}
                      required
                    />
                  </div>
                  <Button type="submit">Submit Review</Button>
                </form>
              </CardContent>
            </Card>
          )}

          {/* Reviews List */}
          <div className="space-y-4">
            {reviews.length === 0 ? (
              <p className="text-gray-600">No reviews yet. Be the first to review!</p>
            ) : (
              reviews.map((review) => (
                <Card key={review._id}>
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center">
                        <span className="font-semibold">{review.user_email}</span>
                        <div className="ml-4 flex text-yellow-500">
                          {"★".repeat(review.rating)}
                          {"☆".repeat(5 - review.rating)}
                        </div>
                      </div>
                      <span className="text-sm text-gray-500">
                        {new Date(review.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <p className="text-gray-700">{review.comment}</p>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;
