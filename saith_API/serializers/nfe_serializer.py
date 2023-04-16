from rest_framework import serializers
from ..models import NFE

class NFeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFE
        fields = ('id', 'document_seller', 'seller', 'number', 'value_nfe', 'date', 'answered', 'operation_science', 'operation_science_date')

class FullNFeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFE
        fields = '__all__'