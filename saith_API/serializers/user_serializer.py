from rest_framework import serializers
from ..models import Users

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=5)

    class Meta:
        fields = ['email', 'password']

class UserOnlyIdAndName(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ('password', 'created_at', 'updated_at', 'email')