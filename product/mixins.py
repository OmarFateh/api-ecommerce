from product.utils import datetime_to_string

from rest_framework import serializers


class TimestampMixin(serializers.Serializer):
    """
    Timestamp serializer mixin.
    """
    updated_at = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    def get_updated_at(self, obj):
        return datetime_to_string(obj.updated_at)

    def get_created_at(self, obj):
        return datetime_to_string(obj.created_at)