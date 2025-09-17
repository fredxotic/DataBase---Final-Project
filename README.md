# FastAPI & React E-commerce Application

This project is a complete full-stack solution for an e-commerce store. It consists of a FastAPI backend API and a React.js frontend application, demonstrating a full-featured CRUD (Create, Read, Update, Delete) system.

The application allows an admin to manage users, products, and categories through a clean and responsive web interface.

Features
Backend (FastAPI):

A robust RESTful API for managing e-commerce data.

Secure password hashing using passlib to protect user credentials.

Comprehensive CRUD operations for Users, Products, and Categories.

MySQL database integration with a well-structured relational schema.

Frontend (React.js):

A clean and user-friendly admin dashboard.

Intuitive forms for creating and updating data.

Dynamic pages to view and manage lists of users, products, and categories.

Styled with plain CSS for a custom and responsive design.

Project Structure
/
├── backend/
│   ├── .env.example
│   ├── ecommerce_store.sql
│   ├── main.py
│   └── requirements.txt
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   └── pages/
    ├── .gitignore
    ├── package.json
    ├── package-lock.json
    └── README.md

Getting Started
Follow these steps to set up and run the entire application.

1. Set Up the Backend
Navigate to the backend directory:

cd backend

Set up the database:

Ensure you have a MySQL server running (e.g., using Docker, XAMPP, or a local installation).

Execute the ecommerce_store.sql script to create the database and all necessary tables. You can use a tool like MySQL Workbench or the command line:

mysql -u your_username -p < ecommerce_store.sql

Configure environment variables:

Copy the .env.example file to a new file named .env.

Open the new .env file and update the database credentials to match your MySQL setup.

DB_HOST=localhost
DB_NAME=ecommerce_store
DB_USER=root
DB_PASSWORD=your_password

Install dependencies:

pip install -r requirements.txt

Run the FastAPI server:

uvicorn main:app --reload

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000). You can view the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

1. Set Up the Frontend
Open a new terminal window and navigate to the frontend directory:

cd ../frontend

Install dependencies:

npm install

Run the React application:

npm start

The application will open in your web browser at [http://localhost:3000](http://localhost:3000).

With both the backend and frontend servers running, the React application will automatically connect to your API, allowing you to interact with the database in real-time.
