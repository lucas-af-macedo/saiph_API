from rest_framework import serializers
from ..models import Document

class DocumentOnlyIdAndDocument(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ('last_nsu', 'last_batch', 'last_request_nfe')