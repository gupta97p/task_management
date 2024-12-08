# Task Management System

A **Task Management System** built with Django and Django REST Framework (DRF), containerized using Docker for efficient deployment and scalability.

---

## 🌟 Features

- **Backend**: Django, Django REST Framework  
  - User authentication using `rest_framework_simplejwt`  
  - CRUD operations for tasks  
  - Filtering and pagination for task lists  
  - Soft delete for tasks (mark as inactive)  
  - Unit tests for models and APIs  

- **Database**: PostgreSQL  
- **Containerization**: Docker & Docker Compose  
- **Deployment**: Seamless deployment on local and cloud platforms  

---

## 📂 Project Structure

```plaintext
task_management/
│
├── backend/                          
│   ├── task_management/              
│   │   ├── settings.py               
│   │   ├── urls.py                   
│   │   ├── wsgi.py   
|   |   └── asgi.py             
│   ├── task_app/                     
│   │   ├── models.py                 
│   │   ├── views.py                  
│   │   ├── serializers.py            
│   │   ├── filters.py                
│   │   ├── pagination.py             
│   │   └── tests.py                  
│   ├── Dockerfile   
|   ├── docker-compose.yml                
│   └── requirements.txt              
└── frontend 
```
## 🚀 Getting Started
Step 1: Clone the Repository

git clone https://github.com/your-username/task_management.git

cd task_management/backend


Step 2: Set Up Environment Variables
Create a .env file in backend/task_management/ with the following contents:

Database settings

`POSTGRES_DB=task_db`

`POSTGRES_USER=task_user`

`POSTGRES_PASSWORD=task_password`

`DB_HOST=host.docker.internal`

`DB_PORT=9011`


JWT settings

`SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=300`


Step 3: Run with Docker

Build and Start Containers

`docker-compose up --build`

Verify Running Services

`docker ps`

To access the Application

http://localhost:800


## 🛠 Local Development (Without Docker)
Install Dependencies:

`pip install -r requirements.txt`

Apply Migrations:

`python manage.py makemigrations`

`python manage.py migrate`

Run the Server:

`python manage.py runserver`

## 🧪 Running Tests
To run unit tests, use:

`python manage.py test`

## 📚 API Endpoints

- ### POST
    - /api/create/ => Register a new user 
    - /api/login/  => Login and get JWT token
    - /api/tasks/  => Create a new task
- ### GET
    - /api/tasks/  => List tasks with filters
- ### Patch
    - /api/tasks/< id:int >/ => Update a specific task
- ### DELETE 
    - /api/tasks/:id/ => Soft-delete a task
