from .models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    User model serializer.
    """
    url = serializers.HyperlinkedIdentityField(view_name='users-api:detail', lookup_field='id')

    class Meta:
        model  = User
        fields = ["id", "first_name", "last_name", "email", "url"]