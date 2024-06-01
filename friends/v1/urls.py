from django.urls import path

from friends.v1.views.friend_request import (
    ListFriendsView, ListPendingFriendRequestsView, 
    RespondFriendRequestView, SendFriendRequestView)


urlpatterns = [
    path('send-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('respond-request/<int:id>/', RespondFriendRequestView.as_view(), name='respond-request'),
    path('friend-list/', ListFriendsView.as_view(), name='list-friends'),
    path('request-pending/', ListPendingFriendRequestsView.as_view(), name='list-pending-requests'),
]
