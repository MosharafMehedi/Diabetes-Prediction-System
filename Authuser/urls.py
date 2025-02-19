from django.urls import path, include
from . import views


urlpatterns = [
   
   path ('registration/',views.registration, name='registration'),
   
   path ('accounts/login/',views.UserLoginView.as_view(), name='login'),
   
   path ('userlogout/',views.user_logout, name='userlogout'),
   
   
]