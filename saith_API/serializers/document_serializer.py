from rest_framework import serializers
from ..models import Document, User_Document_Valid

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ('last_nsu', 'last_batch', 'last_request_nfe')

class DocumentOnlyIdAndDocument(serializers.ModelSerializer):
    document = DocumentSerializer(read_only=True)
    class Meta:
        model = User_Document_Valid
        fields = ('id', 'document')

class UserDocumentOnlyValidSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Document_Valid
        fields = ('id', 'is_valid', 'document_id', 'user_id')

class FullDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'