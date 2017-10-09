import pytz

from rest_framework import serializers


class TimezoneField(serializers.Field):
    """Timezone field for drf."""

    def to_representation(self, obj):
        """obj to str"""
        return obj.zone

    def to_internal_value(self, data):
        """str to obj"""
        if not data:
            raise serializers.ValidationError('This field may not be blank.')
        try:
            return pytz.timezone(data)
        except pytz.exceptions.UnknownTimeZoneError as e:
            raise serializers.ValidationError(e)
