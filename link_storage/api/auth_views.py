from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, PasswordChangeSerializer, PasswordResetSerializer, EmptySerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
import random
import string


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class PasswordChangeView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)


class PasswordResetView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        all_symbols = string.ascii_uppercase + string.digits
        new_password = ''.join(random.choice(all_symbols) for _ in range(9))
        user.set_password(new_password)
        user.save()

        send_mail(
            'Password Reset Request',
            # тут можно реализовать сброс пароля по ссылке
            # f'Click the link to reset your password: http://example.com/reset/{uid}/{token}/',
            f'Your Password is {new_password}',
            f'sapunowdany@yandex.by',
            [email],
            fail_silently=False,
        )
        return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)


class CustomLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]  # Доступно всем


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header:
            return Response({"detail": "Authorization header is missing."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Получаем токен из заголовка Authorization
            token = auth_header.split()[1]
            # Проверяем действительность токена
            AccessToken(token)

            # Получаем экземпляр OutstandingToken
            outstanding_token = OutstandingToken.objects.get(token=token)

            # Добавляем токен в черный список
            BlacklistedToken.objects.create(token=outstanding_token)

            return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except (IndexError, TokenError):
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        except OutstandingToken.DoesNotExist:
            return Response({"detail": "Token not found."}, status=status.HTTP_404_NOT_FOUND)
