from rest_framework import serializers

from ..auth.fields import TimezoneField
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""

    tz = TimezoneField()

    class Meta:
        model = User
        fields = ('pk', 'email', 'name', 'tz', 'exp', 'level', 'date_joined')
        read_only_fields = ('pk', 'email', 'exp', 'level', 'date_joined')
