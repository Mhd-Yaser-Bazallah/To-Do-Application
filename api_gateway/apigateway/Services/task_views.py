import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from apigateway.permissions import IsUser
from dotenv import load_dotenv
import os
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

load_dotenv()

class TaskServiceView(APIView):
 
    permission_classes = [IsUser]

    def _forward_request(self, method, url_suffix, request, **kwargs):
        task_service_url = f"{os.getenv('TASK_SERVICE_URL')}{url_suffix}"
        auth_header = request.headers.get('Authorization')
        headers = {'Authorization': auth_header} if auth_header else {}
        response = requests.request(
            method,
            task_service_url,
            headers=headers,
            json=request.data if method in ['POST', 'PUT','GET',"DELETE"] else None,
            params=request.query_params,
            **kwargs
        )

        return Response(response.json(), status=response.status_code)

    @swagger_auto_schema(
        security=[{'JWT': []}],
        responses={
            200: "Returns list of all tasks",
            404: "No tasks found"
        },
        operation_description="Get all tasks"
    )
    def get(self, request):
        """
        Retrieve all tasks
        """
        print(111111)
        return self._forward_request('GET', '/tasks/', request)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'owner_id': openapi.Schema(type=openapi.TYPE_NUMBER) 
            },
            required=['title']
        ),
        responses={
            201: "Task created successfully",
            400: "Invalid input"
        }
    )
    def post(self, request):
        """
        Create a new task
        """
        return self._forward_request('POST', '/tasks/', request)

     
class TaskDetailView(APIView):
    """
    API View for managing a specific task by ID
    """
    permission_classes = [IsUser]

    def _forward_request(self, method, url_suffix, request, **kwargs):
        task_service_url = f"{os.getenv('TASK_SERVICE_URL')}{url_suffix}"
        auth_header = request.headers.get('Authorization')
        headers = {'Authorization': auth_header} if auth_header else {}

        response = requests.request(
            method,
            task_service_url,
            headers=headers,
            json=request.data if method in ['PUT'] else None,
            params=request.query_params,
            **kwargs
        )

        if response.status_code == 204:  # DELETE success with no content
            return Response({"message": "Task deleted successfully"}, status=204)

        return Response(response.json(), status=response.status_code)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('task_id', openapi.IN_PATH, description="ID of the task to retrieve", type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            200: "Returns requested task",
            404: "Task not found"
        },
        operation_description="Retrieve a specific task by ID"
    )
    def get(self, request, task_id):
        """
        Retrieve a specific task by ID
        """
        return self._forward_request('GET', f'/tasks/{task_id}/', request)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('task_id', openapi.IN_PATH, description="ID of the task to update", type=openapi.TYPE_INTEGER, required=True),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'completion_status': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            }
        ),
        responses={
            200: "Task updated successfully",
            404: "Task not found"
        },
        operation_description="Update a task by ID"
    )
    def put(self, request, task_id):
        """ 
        Update an existing task
        """
        return self._forward_request('PUT', f'/tasks/{task_id}/', request)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('task_id', openapi.IN_PATH, description="ID of the task to delete", type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            204: "Task deleted successfully",
            404: "Task not found"
        },
        operation_description="Delete a task by ID"
    )
    def delete(self, request, task_id):
        """
        Delete a task
        """
        return self._forward_request('DELETE', f'/tasks/{task_id}/', request)
    

class UserTasksView(APIView):
    """
    API View for managing user-specific task operations
    """
    permission_classes = [IsUser]

    def _forward_request(self, method, url_suffix, request, **kwargs):
        task_service_url = f"{os.getenv('TASK_SERVICE_URL')}{url_suffix}"
        print(task_service_url)
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('jwt='):
            token = auth_header.split('=')[1]
            headers = {'Authorization': f'Bearer {token}'}
        else:
            headers = {}

        response = requests.request(
            method,
            task_service_url,
            headers=headers,
            json=request.data if method in ['POST', 'PUT'] else None,
            params=request.query_params,
            **kwargs
        )

        return Response(response.json(), status=response.status_code)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="ID of the user whose tasks to retrieve", type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            200: "Returns user's tasks",
            404: "No tasks found for user"
        }
    )
    def get(self, request, user_id):
        """
        Retrieve all tasks for a specific user
        """
        return self._forward_request('GET', f'/tasks/user/{user_id}/', request) 

