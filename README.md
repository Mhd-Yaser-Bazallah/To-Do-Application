# To-Do-Application
This is a distributed To-Do application built using Django (API Gateway and Authentication Service) 
and FastAPI (Task Service). 
The system is designed to handle user authentication, task management, and event-driven communication between services using RabbitMQ.
________________________________________
#Architecture Overview

The application consists of three main services:

1.	API Gateway:
	Acts as the entry point for all incoming requests.
	Handles authentication, authorization, and routing to the appropriate microservices.
	Built using Django and Django REST Framework.

2.	Authentication Service:
	Manages user registration and login.
	Generates JWT tokens for authenticated users.
	Emits user_created events to RabbitMQ when a new user is registered.
	Built using Django and Django REST Framework.
2.	Task Service:
	Manages tasks (create, read, update, delete).
	Listens for user_created events from RabbitMQ to create corresponding users in its database.
	Built using FastAPI.
________________________________________
#Technologies Used
•	Backend Frameworks:
	Django (API Gateway and Authentication Service)
	FastAPI (Task Service)
 
•	Database:
	SQLite (for simplicity, can be replaced with PostgreSQL or MySQL)
 
•	Message Broker:
	RabbitMQ (for event-driven communication)
 
•	Authentication:
	JWT (JSON Web Tokens)
 
•	API Documentation:
	Swagger (via drf-yasg for Django and built-in FastAPI support)
 
•	Environment Management:
	.env files for environment variables
________________________________________
#Setup Instructions
Prerequisites

1.	Docker:
	
   	Ensure Docker is installed on your machine.
	
 	RabbitMQ will be run using Docker.

2.	Python:
   
	Ensure Python 3.8+ is installed.
________________________________________
#Environment Variables
Each service requires a .env file for configuration. Below are the required variables:

Authentication Service
Create a .env file in the Authentication_Service directory with the following content:

	.env
	DB_NAME=./db.sqlite3
	JWT_SECRET=yaserbazallah

API Gateway
Create a .env file in the api_gateway directory with the following content:

	.env 
	TASK_SERVICE_URL=http://127.0.0.1:8000
	AUTH_SERVICE_URL=http://127.0.0.1:8001
	JWT_SECRET=yaserbazallah
 
________________________________________
#Running the Services
1. Run the RabbitMQ container using Docker
   
	```bash
			        docker pull rabbitmq:3-management
			  	docker run -d --hostname my-rabbit --name some-rabbit -p 8080:15672 -p 5672:5672 rabbitmq:3-management

 	
2.	Authentication Service:
	Navigate to the Authentication_Service directory.
	Install dependencies:

       ```bash
	       			pip install -r requirements.txt
Run the service:

      ```bash
				python manage.py runserver 8001

3.	API Gateway:
	Navigate to the api_gateway directory.
	Install dependencies:

	 ```bash
		pip install -r requirements.txt

Run the service:

    ```bash
   			python manage.py runserver 8002

4.	Task Service:
	Navigate to the Task_Service directory.
	Install dependencies:

        ```bash	
		pip install -r requirements.txt

	Run the service:
	 
     ```bash
		 uvicorn main:app --reload

________________________________________
API Documentation
•	API Gateway:
	Access Swagger documentation at http://localhost:8002/swagger/.
________________________________________
Workflow
1.	User Registration:
	A user registers via the API Gateway (/authentication/register).
	The Authentication Service creates the user, generates a JWT token, and emits a user_created event to RabbitMQ.
	The Task Service listens for the event and creates a corresponding user in its database.

2.	User Login:
	A user logs in via the API Gateway (/authentication/login).
	The Authentication Service validates the credentials and returns a JWT token.
3.	Task Management:
	Authenticated users can perform CRUD operations on tasks via the API Gateway.
	The API Gateway forwards these requests to the Task Service.
________________________________________
Best Practices Followed
1.	Separation of Concerns:
	Each service has a clear responsibility (e.g., authentication, task management).
2.	Event-Driven Architecture:
	RabbitMQ is used for communication between services, ensuring loose coupling.
3.	Environment Variables:
	Sensitive configuration is stored in .env files.
4.	API Documentation:
	Swagger is used for API documentation, making it easy for developers to understand and use the APIs.
5.	Error Handling:
	Proper error handling is implemented in all services.

