from django.urls import path
from .views import RegisterAPIView, VerifEmail, LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email-verify/', VerifEmail.as_view(), name='email-verify'),
]