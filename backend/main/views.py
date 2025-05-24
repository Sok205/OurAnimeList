"""
Django views for the main app
"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        operation_description="Register a new user",
        responses={
            201: openapi.Response(
                description="User created successfully",
                examples={
                    "application/json": {
                        "message": "User registered successfully",
                        "user_id": 1,
                        "username": "example_user",
                        "email": "user@example.com"
                    }
                }
            ),
            400: "Bad Request - Invalid data"
        }
    )

    def post(self, request):
        """
        Register a new user with email and password validation.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'User registered successfully',
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_description="Login a user",
        responses={
            200: openapi.Response(
                description="User logged in successfully",
                examples={
                    "application/json": {
                        "message": "Login successful",
                        "token": "your_jwt_token_here"
                    }
                }
            ),
            400: "Bad Request - Invalid credentials"
        }
    )

    def post(self, request):
        """
        Login a user and return a JWT token.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.get_token()
            return Response(
                {
                    'message': 'Login successful',
                    'token': token
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiRoot(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        """
        Returns a list of available API endpoints.
        """

        content = {
                'message': 'Weeb API - Get your favourite anime!',
                'endpoints': {
                    'token_obtain_pair': '/api/token/',
                    'token_refresh': '/api/token/refresh/',
                    'register': '/api/register/',
                    'login': '/api/login/',
                }
            }

        return Response(content)