from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.db.models import Q

from friends.models import FriendRequest
from user_profile.models import UserProfile
from friends.v1.serializers.friend_request_serializer import FriendRequestSerializer
from user_profile.v1.serializers.user_registration_serializer import UserSearchSerializer


class SendFriendRequestView(generics.CreateAPIView):
    """
    API to send a friend request.
    Ensures that a user cannot send more than 3 friend requests within a minute.
    """
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Handle POST request to send a friend request.
        param:
        request (Request): The request object containing user data.
        Returns:
        Response: The response object with created friend request data or error messages.
        """
        try:
            super().create(request, *args, **kwargs)
            return Response({
                    'message': 'Request has been sent successfully',
                    'status': 'S'
                }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(
                {"errors": e.detail, "status":"F"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"errors": str(e), "status":"F"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class RespondFriendRequestView(generics.UpdateAPIView):
    """
    API to accept or reject a friend request.
    """
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = FriendRequest.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        """
        Handle PUT request to respond to a friend request.
        param:
        request (Request): The request object containing user data.
        id (int): The ID of the friend request to respond to.
        Returns:
        Response: The response object with updated friend request data or error messages.
        """
        
        instance = self.get_object()
        if instance.to_user != request.user:
            return Response(
                {"error": "You cannot respond to this friend request.",
                 "status": "F"
                 }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            request_data = request.data
            if instance.status != request_data.get('status'):
                instance.status = request_data.get('status', FriendRequest.REQUEST_PENDING)
                instance.save()
            return Response({"status": "S", "message": "Friend request has been updated."}, 
                            status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"errors": e.detail, "status": "F"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors": str(e), "status": "F"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ListFriendsView(generics.ListAPIView):
    """
    API to list friends (accepted friend requests).
    """
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the list of friends for the authenticated user.
        Returns:
        Queryset of active users who are friends with the authenticated user.
        """
        user = self.request.user
        friend_requests = FriendRequest.objects.filter(
            Q(created_by=user, status=FriendRequest.REQUEST_ACCEPTED) 
        )
        friend_ids = friend_requests.values_list('to_user_id')
        queryset = UserProfile.objects.filter(id__in=friend_ids, is_active=True)
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
                "data": response.data,
                'status': 'S'
            }, status=status.HTTP_200_OK)
    

class ListPendingFriendRequestsView(generics.ListAPIView):
    """
    API to list pending friend requests (received).
    """
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the list of pending friend requests for the authenticated user.
        Returns:
        Queryset of pending friend requests received by the authenticated user from active users.
        """
        user = self.request.user
        queryset = FriendRequest.objects.filter(
            to_user=user, status=FriendRequest.REQUEST_PENDING, created_by__is_active=True)
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
                "data": response.data,
                'status': 'S'
            }, status=status.HTTP_200_OK)
