from allauth.account.models import EmailAddress

from django.contrib.auth import logout
from django.shortcuts import get_object_or_404

from rest_framework import permissions, response, status, viewsets

from .serializers import UserSerializer
from ..models import User


class UserViewSet(viewsets.GenericViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request, pk=None):
        if pk == 'me':
            if not request.user.is_authenticated:
                return response.Response(status=status.HTTP_403_FORBIDDEN)
            user = request.user
        else:
            queryset = self.get_queryset()
            user = get_object_or_404(queryset, pk=pk)
        if user.is_active:
            serializer = self.get_serializer(user)
            return response.Response(serializer.data)
        else:
            return response.Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, pk=None):
        if pk == 'me' or request.user.pk == pk:
            if not request.user.is_authenticated:
                return response.Response(status=status.HTTP_403_FORBIDDEN)
            user = request.user
            serializer = self.get_serializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.Response(
                    {'detail': 'Saved.'},
                    status=status.HTTP_202_ACCEPTED
                )
            else:
                return response.Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return response.Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        if pk == 'me' or request.user.pk == pk:
            if request.user.is_anonymous:
                return response.Response(status=status.HTTP_403_FORBIDDEN)
            user = request.user
            out_sign = f'out_{user.pk}@out.out'
            user.name = '탈퇴회원'
            user.email = out_sign
            user.tz = 'Asia/Seoul'
            user.is_active = False
            user.save()

            addresses = EmailAddress.objects.filter(user=user)
            for address in addresses:
                address.email = out_sign
                address.save()

            try:
                logout(request)
            except AttributeError:
                pass

            return response.Response(
                {'detail': 'Done.'},
                status=status.HTTP_202_ACCEPTED
            )
        else:
            return response.Response(status=status.HTTP_403_FORBIDDEN)
