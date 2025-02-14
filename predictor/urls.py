from django.contrib import admin
from django.urls import path
from predictor import views

urlpatterns = [
    
    path('predict/', views.predict, name='predict'),
    
    
]