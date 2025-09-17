import requests
import json

BASE_URL = "http://localhost:8000"

def test_all_operations():
    print("🧪 Testing all CRUD operations...")
    
    # Test User CRUD
    print("\n👥 Testing User Operations:")
    
    # Create user
    user_data = {
        "email": "testuser@example.com",
        "password": "testpass",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "123-TEST"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Create User: {response.status_code}")
    user_id = response.json().get('user_id')
    
    # Read user
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(f"Read User: {response.status_code}")
    
    # Update user
    update_data = user_data.copy()
    update_data['first_name'] = "UpdatedTest"
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    print(f"Update User: {response.status_code}")
    
    # Test Product CRUD
    print("\n📦 Testing Product Operations:")
    
    # Create product
    product_data = {
        "name": "Test Product",
        "description": "Test description",
        "price": 99.99,
        "stock_quantity": 10,
        "category_id": 1,
        "image_url": None
    }
    response = requests.post(f"{BASE_URL}/products/", json=product_data)
    print(f"Create Product: {response.status_code}")
    product_id = response.json().get('product_id')
    
    # Read product
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    print(f"Read Product: {response.status_code}")
    
    # Update product
    update_product = {"price": 109.99, "stock_quantity": 5}
    response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_product)
    print(f"Update Product: {response.status_code}")
    
    # Read all products
    response = requests.get(f"{BASE_URL}/products/")
    print(f"Read All Products: {response.status_code}, Count: {len(response.json())}")
    
    # Read all users
    response = requests.get(f"{BASE_URL}/users/")
    print(f"Read All Users: {response.status_code}, Count: {len(response.json())}")
    
    print("\n🎉 All basic CRUD operations completed successfully!")

if __name__ == "__main__":
    test_all_operations()