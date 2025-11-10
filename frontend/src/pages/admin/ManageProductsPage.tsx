import React, { useEffect, useState } from "react";
import api from "../../api/axios";
import { Product } from "../../types";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";

const ManageProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await api.get("/products?limit=1000");
      setProducts(response.data.products);
    } catch (error) {
      console.error("Error fetching products:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this product?")) return;

    try {
      await api.delete(`/admin/products/${id}`);
      setProducts(products.filter((p) => p._id !== id));
      alert("Product deleted successfully");
    } catch (error) {
      console.error("Error deleting product:", error);
      alert("Failed to delete product");
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold">Manage Products</h1>
          <Button onClick={() => window.location.href = "/admin/products/new"}>
            Add New Product
          </Button>
        </div>

        <div className="space-y-4">
          {products.map((product) => (
            <Card key={product._id}>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <img
                      src={product.image_url}
                      alt={product.name}
                      className="w-20 h-20 object-cover rounded"
                    />
                    <div>
                      <h3 className="font-semibold text-lg">{product.name}</h3>
                      <p className="text-sm text-gray-600">{product.category}</p>
                      <div className="flex gap-4 mt-2">
                        <span className="text-sm">
                          <strong>Price:</strong> ${product.price.toFixed(2)}
                        </span>
                        <span className="text-sm">
                          <strong>Stock:</strong> {product.stock_quantity}
                        </span>
                        <span className="text-sm">
                          <strong>Rating:</strong> {product.avg_rating.toFixed(1)}★
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      onClick={() => window.location.href = `/admin/products/${product._id}/edit`}
                    >
                      Edit
                    </Button>
                    <Button variant="destructive" onClick={() => handleDelete(product._id)}>
                      Delete
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ManageProductsPage;
