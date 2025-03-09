from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from .services import AuthService
from .repositories import UserRepository
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import traceback

class BaseAuthView(APIView):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService(UserRepository())   

class RegisterView(BaseAuthView):
    def post(self, request):
        try:
            print("Registration data received:", request.data)
            serializer = RegisterSerializer(data=request.data)
            
            if not serializer.is_valid():
                print("Validation errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            token_data = self.auth_service.register_user(serializer)       
            response = Response(token_data, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='jwt',
                value=token_data['token'],
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=3600
            )
            return response
            
        except Exception as e:
            print("Registration error:", str(e))
            print("Traceback:", traceback.format_exc())
            return Response(
                {"error": "Registration failed", "detail": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(BaseAuthView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            token_data = self.auth_service.login_user(email, password)
            response = Response(token_data, status=status.HTTP_200_OK)
            response.set_cookie(
                key='jwt',
                value=token_data['token'],
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=3600
            )
            return response
            
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print("Login error:", str(e))
            print("Traceback:", traceback.format_exc())
            return Response(
                {"error": "Login failed", "detail": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    