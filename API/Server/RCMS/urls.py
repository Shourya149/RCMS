from django.urls import path 
from .views import *

#Registering our routes
urlpatterns = [
    path('signup',SignUpView.as_view()),
    path('signin',SignInView.as_view()),
    path('expired',TokenExpiredView.as_view()),
    path('bid',BiddingView.as_view()),
]