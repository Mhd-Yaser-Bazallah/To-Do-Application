import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from dotenv import load_dotenv
import os
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
import traceback
 
load_dotenv()
    
class AuthServiceView(APIView):
    """
    API View for handling authentication operations
    """
    def _forward_request(self, method, url_suffix, request, **kwargs):
        try:
            auth_service_url = f"{os.getenv('AUTH_SERVICE_URL')}/{url_suffix.lstrip('/')}" 
            request_data = dict(request.data.items()) if hasattr(request.data, 'items') else request.data
            if 'register' in url_suffix and 'username' in request_data:
                request_data['name'] = request_data['username']
            response = requests.request(
                method,
                auth_service_url,
                headers={
                    'Authorization': request.headers.get('Authorization'),
                    'Content-Type': 'application/json'
                },
                json=request_data if method in ['POST', 'PUT'] else None,
                params=request.query_params,
                **kwargs
            )
            
 
            
            try:
                return Response(response.json(), status=response.status_code)
            except json.JSONDecodeError:
                error_message = response.text or "No error details available"
                
                return Response(
                    {
                        "error": "Invalid response from authentication service",
                        "detail": error_message,
                        "status_code": response.status_code
                    },
                    status=response.status_code
                )
                
        except requests.RequestException as e:
            return Response(
                {"error": "Failed to connect to authentication service", "detail": str(e)},
                status=500
            )
        except Exception as e:
            return Response(
                {"error": "Internal server error", "detail": str(e)},
                status=500
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('action', openapi.IN_PATH, description="Authentication action (register or login)", type=openapi.TYPE_STRING, required=True, enum=['register', 'login']),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username for authentication'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for authentication'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email (required for registration)'),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description='JWT token (returned for login)'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    }
                )
            ),
            400: "Invalid request or credentials",
            401: "Authentication failed",
            500: "Internal server error"
        },
        operation_description="""
        Handle authentication operations:
        - register: Create a new user account
        - login: Authenticate and receive JWT token
        """
    )

    def post(self, request, action=None):
        """
        Handle user registration and login
        """
        if action == 'register' and 'username' in request.data:
            mutable_data = request.data.copy()
            mutable_data['name'] = mutable_data.pop('username')
            request._full_data = mutable_data

        if action == 'register':
            return self._forward_request('POST', 'authentication/register', request)
        elif action == 'login':
            return self._forward_request('POST', '/authentication/login', request)
        else:
            return Response({"error": "Invalid action"}, status=400)
