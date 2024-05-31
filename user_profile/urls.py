from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('user_profile.v1.urls'))
]
