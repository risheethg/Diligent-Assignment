"""Database initialization and seeding."""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.models.user import User
from app.models.product import Product
from app.models.review import Review
from app.models.order import Order
from app.models.cart import Cart


async def init_db():
    """Initialize database connection and beanie ODM."""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client.get_default_database()
    
    await init_beanie(
        database=database,
        document_models=[
            User,
            Product,
            Review,
            Order,
            Cart
        ]
    )
    
    print("Database initialized successfully!")


async def seed_database():
    """Seed the database with sample products if empty."""
    # Check if products already exist
    product_count = await Product.count()
    
    if product_count > 0:
        print(f"Database already has {product_count} products. Skipping seed.")
        return
    
    print("Seeding database with sample products...")
    
    sample_products = [
        {
            "name": "Wireless Bluetooth Headphones",
            "description": "Premium noise-cancelling over-ear headphones with 30-hour battery life. Deep bass, crystal clear highs, and comfortable ear cushions for all-day wear.",
            "price": 89.99,
            "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop",
            "category": "Electronics",
            "stock_quantity": 50
        },
        {
            "name": "Ergonomic Office Chair",
            "description": "Adjustable lumbar support office chair with breathable mesh back. 360-degree swivel, adjustable height, and armrests for maximum comfort during long work sessions.",
            "price": 249.99,
            "imageUrl": "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=500&h=500&fit=crop",
            "category": "Furniture",
            "stock_quantity": 25
        },
        {
            "name": "Stainless Steel Water Bottle",
            "description": "Insulated 32oz water bottle keeps drinks cold for 24 hours or hot for 12 hours. BPA-free, leak-proof design with wide mouth for easy cleaning.",
            "price": 24.99,
            "imageUrl": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&h=500&fit=crop",
            "category": "Home & Kitchen",
            "stock_quantity": 100
        },
        {
            "name": "Mechanical Gaming Keyboard",
            "description": "RGB backlit mechanical keyboard with Cherry MX Blue switches. Full N-key rollover, aluminum frame, and programmable macro keys for gaming enthusiasts.",
            "price": 129.99,
            "imageUrl": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&h=500&fit=crop",
            "category": "Electronics",
            "stock_quantity": 40
        },
        {
            "name": "Yoga Mat with Carrying Strap",
            "description": "Extra thick 6mm yoga mat with non-slip surface. Eco-friendly TPE material, lightweight, and includes carrying strap for easy transport.",
            "price": 34.99,
            "imageUrl": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500&h=500&fit=crop",
            "category": "Sports & Outdoors",
            "stock_quantity": 75
        },
        {
            "name": "Smart Watch Fitness Tracker",
            "description": "Advanced fitness tracking with heart rate monitor, sleep tracking, and GPS. 7-day battery life, water-resistant, and compatible with iOS and Android.",
            "price": 199.99,
            "imageUrl": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop",
            "category": "Electronics",
            "stock_quantity": 60
        },
        {
            "name": "Premium Coffee Maker",
            "description": "Programmable 12-cup coffee maker with thermal carafe. Brew strength control, auto shut-off, and permanent filter included.",
            "price": 79.99,
            "imageUrl": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500&h=500&fit=crop",
            "category": "Home & Kitchen",
            "stock_quantity": 35
        },
        {
            "name": "Leather Laptop Backpack",
            "description": "Professional leather backpack with padded laptop compartment (fits up to 15.6 inch). Multiple pockets, USB charging port, and water-resistant design.",
            "price": 89.99,
            "imageUrl": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop",
            "category": "Bags & Accessories",
            "stock_quantity": 45
        },
        {
            "name": "Wireless Gaming Mouse",
            "description": "High-precision wireless mouse with 16,000 DPI sensor. Customizable RGB lighting, 8 programmable buttons, and 70-hour battery life.",
            "price": 69.99,
            "imageUrl": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=500&h=500&fit=crop",
            "category": "Electronics",
            "stock_quantity": 80
        },
        {
            "name": "Portable Bluetooth Speaker",
            "description": "Waterproof portable speaker with 360-degree sound. 12-hour playtime, deep bass, and built-in microphone for hands-free calls.",
            "price": 49.99,
            "imageUrl": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&h=500&fit=crop",
            "category": "Electronics",
            "stock_quantity": 90
        },
        {
            "name": "Dumbbell Set with Rack",
            "description": "Adjustable dumbbell set from 5-50 lbs with storage rack. Space-saving design, quick-change weight selection, perfect for home gym.",
            "price": 299.99,
            "imageUrl": "https://images.unsplash.com/photo-1599058917212-d750089bc07e?w=500&h=500&fit=crop",
            "category": "Sports & Outdoors",
            "stock_quantity": 20
        },
        {
            "name": "Standing Desk Converter",
            "description": "Height-adjustable standing desk converter. Smooth lift mechanism, spacious workspace, and keyboard tray for ergonomic comfort.",
            "price": 179.99,
            "imageUrl": "https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?w=500&h=500&fit=crop",
            "category": "Furniture",
            "stock_quantity": 30
        },
        {
            "name": "Air Purifier with HEPA Filter",
            "description": "3-stage filtration air purifier removes 99.97% of airborne particles. Quiet operation, smart sensor, and covers up to 500 sq ft.",
            "price": 149.99,
            "imageUrl": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=500&h=500&fit=crop",
            "category": "Home & Kitchen",
            "stock_quantity": 40
        },
        {
            "name": "USB-C Hub Multi-Adapter",
            "description": "7-in-1 USB-C hub with HDMI 4K, USB 3.0 ports, SD card reader, and 100W power delivery. Compact and travel-friendly design.",
            "price": 39.99,
            "imageUrl": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=500&h=500&fit=crop",
            "category": "Electronics",
            "stock_quantity": 120
        },
        {
            "name": "Memory Foam Pillow Set",
            "description": "2-pack premium memory foam pillows with cooling gel layer. Hypoallergenic, adjustable loft, and machine-washable covers.",
            "price": 59.99,
            "imageUrl": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=500&h=500&fit=crop",
            "category": "Home & Kitchen",
            "stock_quantity": 65
        }
    ]
    
    products = [Product(**product_data) for product_data in sample_products]
    await Product.insert_many(products)
    
    print(f"Successfully seeded {len(products)} products!")
