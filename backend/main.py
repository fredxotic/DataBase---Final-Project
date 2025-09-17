from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv
import traceback
from passlib.context import CryptContext

load_dotenv()

app = FastAPI(title="E-commerce Store API", version="1.0.0")

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Database connection
def get_db_connection():
    """Establishes and returns a new database connection."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'ecommerce_store'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            autocommit=False
        )
        return connection
    except Error as e:
        print(f"❌ Database connection failed: {str(e)}")
        print(f"❌ Connection details: host={os.getenv('DB_HOST')}, db={os.getenv('DB_NAME')}, user={os.getenv('DB_USER')}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    user_id: int
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
    created_at: datetime
    updated_at: datetime

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    category_id: int
    image_url: Optional[str] = None

class ProductResponse(BaseModel):
    product_id: int
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int
    category_id: int
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    image_url: Optional[str] = None

class CategoryResponse(BaseModel):
    category_id: int
    name: str
    description: Optional[str]
    parent_category_id: Optional[int]

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    parent_category_id: Optional[int] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_category_id: Optional[int] = None

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to E-commerce Store API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "users": "/users",
            "products": "/products",
            "categories": "/categories"
        }
    }

# Health check endpoint
@app.get("/health")
def health_check():
    try:
        connection = get_db_connection()
        connection.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Users CRUD Operations
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash the password before storing
        hashed_password = pwd_context.hash(user.password)

        # Insert new user
        query = """
            INSERT INTO users (email, password_hash, first_name, last_name, phone_number)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user.email, hashed_password, user.first_name, user.last_name, user.phone_number))
        connection.commit()
        
        # Get the created user
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (cursor.lastrowid,))
        created_user = cursor.fetchone()
        
        return created_user
        
    except Error as e:
        connection.rollback()
        print(f"❌ Database error in create_user: {str(e)}")
        print(f"❌ Error details: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
        
    except Error as e:
        print(f"❌ Database error in get_user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.get("/users/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 10):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM users LIMIT %s OFFSET %s", (limit, skip))
        users = cursor.fetchall()
        return users
        
    except Error as e:
        print(f"❌ Database error in get_users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        existing_user = cursor.fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Build dynamic update query
        update_fields = []
        update_values = []
        
        if user_update.email is not None:
            # Check for unique email
            cursor.execute("SELECT * FROM users WHERE email = %s AND user_id != %s", (user_update.email, user_id))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Email already registered by another user")
            update_fields.append("email = %s")
            update_values.append(user_update.email)
        
        if user_update.password is not None:
            # Hash the new password
            hashed_password = pwd_context.hash(user_update.password)
            update_fields.append("password_hash = %s")
            update_values.append(hashed_password)
        
        if user_update.first_name is not None:
            update_fields.append("first_name = %s")
            update_values.append(user_update.first_name)
        
        if user_update.last_name is not None:
            update_fields.append("last_name = %s")
            update_values.append(user_update.last_name)
        
        if user_update.phone_number is not None:
            update_fields.append("phone_number = %s")
            update_values.append(user_update.phone_number)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_values.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = %s"
        
        cursor.execute(query, update_values)
        connection.commit()
        
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        updated_user = cursor.fetchone()
        
        return updated_user
        
    except Error as e:
        connection.rollback()
        print(f"❌ Database error in update_user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        connection.commit()
        
        return {"message": "User deleted successfully"}
        
    except Error as e:
        connection.rollback()
        print(f"❌ Database error in delete_user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Products CRUD Operations
@app.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Check if category exists
        cursor.execute("SELECT * FROM categories WHERE category_id = %s", (product.category_id,))
        category = cursor.fetchone()
        if not category:
            raise HTTPException(status_code=400, detail=f"Category with ID {product.category_id} does not exist")
        
        # Insert product
        query = """
            INSERT INTO products (name, description, price, stock_quantity, category_id, image_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            product.name, product.description, product.price, 
            product.stock_quantity, product.category_id, product.image_url
        ))
        connection.commit()
        
        # Get the created product
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (cursor.lastrowid,))
        created_product = cursor.fetchone()
        
        return created_product
        
    except Error as e:
        connection.rollback()
        print(f"❌ Database error in create_product: {str(e)}")
        print(f"❌ Error details: {traceback.format_exc()}")
        print(f"❌ Product data: {product.dict()}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        print(f"❌ Unexpected error in create_product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
        
    except Error as e:
        print(f"❌ Database error in get_product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.get("/products/", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 10, category_id: Optional[int] = None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        if category_id:
            cursor.execute("SELECT * FROM products WHERE category_id = %s LIMIT %s OFFSET %s", 
                         (category_id, limit, skip))
        else:
            cursor.execute("SELECT * FROM products LIMIT %s OFFSET %s", (limit, skip))
        
        products = cursor.fetchall()
        return products
        
    except Error as e:
        print(f"❌ Database error in get_products: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Check if product exists
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Build dynamic update query
        update_fields = []
        update_values = []
        
        if product_update.name is not None:
            update_fields.append("name = %s")
            update_values.append(product_update.name)
        if product_update.description is not None:
            update_fields.append("description = %s")
            update_values.append(product_update.description)
        if product_update.price is not None:
            update_fields.append("price = %s")
            update_values.append(product_update.price)
        if product_update.stock_quantity is not None:
            update_fields.append("stock_quantity = %s")
            update_values.append(product_update.stock_quantity)
        if product_update.image_url is not None:
            update_fields.append("image_url = %s")
            update_values.append(product_update.image_url)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_values.append(product_id)
        query = f"UPDATE products SET {', '.join(update_fields)} WHERE product_id = %s"
        
        cursor.execute(query, update_values)
        connection.commit()
        
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        updated_product = cursor.fetchone()
        
        return updated_product
        
    except Error as e:
        connection.rollback()
        print(f"❌ Database error in update_product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Check if product exists
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Product not found")
        
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        connection.commit()
        
        return {"message": "Product deleted successfully"}
        
    except Error as e:
        connection.rollback()
        print(f"❌ Database error in delete_product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Categories endpoints
@app.post("/categories/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """
            INSERT INTO categories (name, description, parent_category_id)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (category.name, category.description, category.parent_category_id))
        connection.commit()
        
        cursor.execute("SELECT * FROM categories WHERE category_id = %s", (cursor.lastrowid,))
        created_category = cursor.fetchone()
        
        return created_category
        
    except Error as e:
        connection.rollback()
        print(f"❌ Database error in create_category: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.get("/categories/", response_model=List[CategoryResponse])
def get_categories():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        return categories
        
    except Error as e:
        print(f"❌ Database error in get_categories: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category_update: CategoryUpdate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Check if category exists
        cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Build dynamic update query
        update_fields = []
        update_values = []
        
        if category_update.name is not None:
            update_fields.append("name = %s")
            update_values.append(category_update.name)
        if category_update.description is not None:
            update_fields.append("description = %s")
            update_values.append(category_update.description)
        if category_update.parent_category_id is not None:
            # Add a check to prevent a category from being its own parent
            if category_update.parent_category_id == category_id:
                raise HTTPException(status_code=400, detail="A category cannot be its own parent.")
            update_fields.append("parent_category_id = %s")
            update_values.append(category_update.parent_category_id)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_values.append(category_id)
        query = f"UPDATE categories SET {', '.join(update_fields)} WHERE category_id = %s"
        
        cursor.execute(query, update_values)
        connection.commit()
        
        cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
        updated_category = cursor.fetchone()
        
        return updated_category
        
    except Error as e:
        connection.rollback()
        print(f"❌ Database error in update_category: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Check if category exists
        cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Category not found")
        
        cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
        connection.commit()
        
        return {"message": "Category deleted successfully"}
        
    except Error as e:
        connection.rollback()
        print(f"❌ Database error in delete_category: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
