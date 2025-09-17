E-Commerce Admin Dashboard
A full-stack e-commerce application built with FastAPI for the backend and React for the frontend, designed to showcase a complete, end-to-end CRUD (Create, Read, Update, Delete) system. This project allows an admin to manage users, products, and categories through a sleek web interface.

🚀 Key Features
FastAPI Backend: A robust and secure RESTful API with endpoints for users, products, and categories.

Secure Authentication: User passwords are securely hashed using passlib.

MySQL Database: A comprehensive relational database schema to support the e-commerce model.

Dynamic CRUD Operations: Flexible update and delete endpoints with proper error handling.

React Frontend: A clean and modern admin dashboard for managing all data.

Component-Based UI: A well-organized structure using React components for reusability.

Responsive Design: A user interface that works seamlessly on desktop and mobile devices.

Intuitive Navigation: A clear and easy-to-use navigation system to switch between different sections.

📁 Folder Structure
The project is organized into two main directories:

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
    ├── package.json
    └── README.md

🛠️ Getting Started
Follow these steps to get the application up and running on your local machine.

1. Backend Setup (FastAPI)
Navigate to the backend directory in your terminal:

cd backend

Set up your MySQL database:

Ensure you have a MySQL server running.

Use a tool like MySQL Workbench or the command line to execute the ecommerce_store.sql script. This will create the ecommerce_store database and all necessary tables.

mysql -u your_username -p < ecommerce_store.sql

Configure Environment Variables:

Create a file named .env in the backend directory.

Copy the contents of .env.example into your new .env file and replace the placeholder values with your actual database credentials.

Install Python dependencies:

pip install -r requirements.txt

Run the API server:

uvicorn main:app --reload

The API will be live at http://127.0.0.1:8000.

2. Frontend Setup (React)
Open a new terminal window and navigate to the frontend directory:

cd frontend

Install Node.js dependencies:

npm install

Run the React development server:

npm start

The admin dashboard will automatically open in your web browser at http://localhost:3000.

With both servers running, the React frontend will seamlessly connect to the FastAPI backend, giving you a complete, working application.
