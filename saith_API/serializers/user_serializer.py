from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=5)

    class Meta:
        fields = ['email', 'password']