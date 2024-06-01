from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('friends.v1.urls'))
]
