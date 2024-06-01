from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from user_profile.v1.serializers.user_registration_serializer import (
    UserRegistrationSerializer, LoginSerializer, UserSearchSerializer)
from user_profile.models import UserProfile
from user_profile.utils import (
    set_jwt_token_cookie, add_access_token_validity_cookie,
    fetch_token_from_header)
from user_profile.v1.pagination import UserListPagination


class UserRegistrationView(generics.CreateAPIView):
    """
    View for user registration.
    Allows a new user to register by providing the required fields.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """
        Handle POST request for user registration.
        :param request: The HTTP request containing user data.
        :return: The HTTP response with user data or error messages.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "User registered successfully.",
                'status': 'S'
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({
                "errors": e.detail,
                "message": "User registration failed.",
                'status': 'F'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "errors": str(e),
                "message": "Something went wrong.",
                'status': 'F'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    """
    View for handling the login process.
    """

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        """
        Method will check the user is valid or not and
        returns success for validated user.
        param: user email and password
        return:
        """
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = authenticate(
                email=serializer.validated_data.get('email'),
                password=serializer.validated_data.get('password')
            )
            if user and user.is_active:
                login(request, user)
                response = Response(status=status.HTTP_200_OK)
                token = self.get_tokens_for_user(user)
                set_jwt_token_cookie(
                    response,
                    token,
                )
                add_access_token_validity_cookie(response)
                response.data = {
                    'message': 'User has been logged in successfully',
                    'token': token['access'],
                    'status': 'S'
                }
                return response
            else:
                return Response({
                "errors": "Invalid credentials.",
                "message": "Failed to login.",
                'status': 'F'
            }, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({
                "errors": e.detail,
                "message": "Failed to login.",
                'status': 'F'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "errors": str(e),
                "message": "Something went wrong.",
                'status': 'F'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle get request for logging out the user.
        """
        try:
            response = Response(status=status.HTTP_200_OK)
            for cookie in request.COOKIES:
                response.delete_cookie(
                    cookie, samesite='None',
                    domain=settings.TOKEN_COOKIE_DOMAIN
                )
            logout(request)
            response.data = {
                    'message': 'User has been logged out successfully.',
                    'status': 'S'
                }
            return response
        except (TokenError, Exception) as e:
            return Response({
                "errors": str(e),
                "message": "Something went wrong.",
                'status': 'F'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserSearchView(generics.ListAPIView):
    """
    API to search users by email or name.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSearchSerializer
    pagination_class = UserListPagination

    def get_queryset(self):
        """
        Get the list of items for this view.
        """
        keyword = self.request.query_params.get('q', '')
        queryset = []
        if keyword:
            filter_condition = (
                Q(email__iexact=keyword) | Q(first_name__icontains=keyword) | 
                Q(last_name__icontains=keyword) & Q(is_active=True))
            queryset = UserProfile.objects.filter(filter_condition)
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
                "data": response.data,
                'status': 'S'
            }, status=status.HTTP_200_OK)

        
