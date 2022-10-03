from django.urls import path
from .views import RegisterAPIView, VerifEmail

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('email-verify/', VerifEmail.as_view(), name='email-verify'),
]