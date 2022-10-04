from urllib import request 
from rest_framework.response import Response
from rest_framework import status, views, generics

from .serializers import RegisterSerializer, VerifyEmailSerializer, LoginSerializer 

from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data 
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data 
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user)

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        
        abs_url = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Salom '+user.username+'Use link below to verify email \n'+abs_url
        data = {'email_body':email_body, 'to_email':user.email, 
                'email_subject': 'Verify your email'}

        # Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifEmail(views.APIView):
    serializer_class = VerifyEmailSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING
        )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Email aktivlashtirildi'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as inedtifier:
            return Response({'error': 'Xatolik aniqlandi'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as inedtifier:
            return Response({'error': 'Tokenda xatolik'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


