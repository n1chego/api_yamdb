import secrets
import string

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.pagination import LimitOffsetPagination

from api_yamdb import settings
from api.permissions import AdminOrRead
from api.serializers import (
                           TokenSerializer,
                           UserSerializer,
                           UserSignUpSerializer,
                        )
from .models import User


class UserSignUpView(CreateAPIView):
    serializer_class = UserSignUpSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        alphabet = string.ascii_letters + string.digits
        code = ''.join(secrets.choice(alphabet) for i in range(8))
        user, _ = User.objects.get_or_create(
            username=serializer.data.get('username'),
            email=serializer.data.get('email'),
            confirmation_code=code
        )
        message = (f'Ваш код подтверждения: {code}')
        send_mail(
            subject='Регистрация на сайте',
            message=message,
            from_email=settings.FROM_EMAIL,
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOrRead,)
    lookup_field = 'username'
    search_fields = ('username',)
    pagination_class = LimitOffsetPagination


    @action(
        ['GET', 'PATCH'], permission_classes=(IsAuthenticated,),
        detail=False, url_path='me'
    )
    def me(self, request):
        if not request.data:
            serializer = self.serializer_class(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.user.role == 'admin':
            serializer.update(request.user, serializer.validated_data)
        else:
            serializer.nonadmin_update(
                request.user, serializer.validated_data
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

class TokenView(TokenViewBase):
    serializer_class = TokenSerializer
