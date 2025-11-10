import React, { useEffect, useState } from "react";
import api from "../../api/axios";
import { Order } from "../../types";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";

const ManageOrdersPage: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await api.get("/admin/orders");
      setOrders(response.data);
    } catch (error) {
      console.error("Error fetching orders:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (orderId: string, status: string) => {
    try {
      await api.patch(`/admin/orders/${orderId}/status`, { status });
      setOrders(
        orders.map((order) =>
          order._id === orderId ? { ...order, status } : order
        )
      );
      alert("Order status updated successfully");
    } catch (error) {
      console.error("Error updating order status:", error);
      alert("Failed to update order status");
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
        <h1 className="text-4xl font-bold mb-8">Manage Orders</h1>

        {orders.length === 0 ? (
          <Card>
            <CardContent className="pt-6">
              <p className="text-xl text-center text-gray-600">No orders yet</p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {orders.map((order) => (
              <Card key={order._id}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-xl">
                        Order #{order._id.slice(-8)}
                      </CardTitle>
                      <p className="text-sm text-gray-600 mt-1">
                        Customer: {order.user_email}
                      </p>
                      <p className="text-sm text-gray-600">
                        Date: {new Date(order.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        order.status === "delivered"
                          ? "bg-green-100 text-green-800"
                          : order.status === "processing"
                          ? "bg-blue-100 text-blue-800"
                          : order.status === "shipped"
                          ? "bg-purple-100 text-purple-800"
                          : "bg-yellow-100 text-yellow-800"
                      }`}
                    >
                      {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                    </span>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {/* Order Items */}
                    <div>
                      <h3 className="font-semibold mb-2">Items:</h3>
                      {order.items.map((item, index) => (
                        <div key={index} className="flex justify-between text-sm mb-2">
                          <span>
                            {item.product_name} x {item.quantity}
                          </span>
                          <span>${(item.price * item.quantity).toFixed(2)}</span>
                        </div>
                      ))}
                    </div>

                    {/* Shipping Address */}
                    <div>
                      <h3 className="font-semibold mb-2">Shipping Address:</h3>
                      <p className="text-sm text-gray-600">
                        {order.shipping_address.street}, {order.shipping_address.city},{" "}
                        {order.shipping_address.state} {order.shipping_address.zipCode},{" "}
                        {order.shipping_address.country}
                      </p>
                    </div>

                    {/* Total */}
                    <div className="border-t pt-4">
                      <div className="flex justify-between font-bold text-lg mb-4">
                        <span>Total:</span>
                        <span>${order.total_amount.toFixed(2)}</span>
                      </div>

                      {/* Status Update Buttons */}
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant={order.status === "pending" ? "default" : "outline"}
                          onClick={() => handleStatusUpdate(order._id, "pending")}
                          disabled={order.status === "pending"}
                        >
                          Pending
                        </Button>
                        <Button
                          size="sm"
                          variant={order.status === "processing" ? "default" : "outline"}
                          onClick={() => handleStatusUpdate(order._id, "processing")}
                          disabled={order.status === "processing"}
                        >
                          Processing
                        </Button>
                        <Button
                          size="sm"
                          variant={order.status === "shipped" ? "default" : "outline"}
                          onClick={() => handleStatusUpdate(order._id, "shipped")}
                          disabled={order.status === "shipped"}
                        >
                          Shipped
                        </Button>
                        <Button
                          size="sm"
                          variant={order.status === "delivered" ? "default" : "outline"}
                          onClick={() => handleStatusUpdate(order._id, "delivered")}
                          disabled={order.status === "delivered"}
                        >
                          Delivered
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ManageOrdersPage;
