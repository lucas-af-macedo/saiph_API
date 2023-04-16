from ..models import User_Document_Valid, NFE
from ..serializers import document_serializer, nfe_serializer

def get_user_document_valid(id, user_id):
    document = User_Document_Valid.objects.filter(id=id, user_id=user_id)
    user_document = document_serializer.UserDocumentOnlyValidSerializer(document, many=True).data
    return user_document

def get_user_document_valid_by_document(document_id, user_id):
    document = User_Document_Valid.objects.filter(document_id=document_id, user_id=user_id)
    user_document = document_serializer.UserDocumentOnlyValidSerializer(document, many=True).data
    return user_document

def insert_many_nfes(list_nfes):
    nfes = NFE.objects.bulk_create(list_nfes)

    return nfes

def get_nfes(document_id):
    nfes = NFE.objects.filter(document_id=document_id)
    nfes_list = nfe_serializer.NFeSerializer(nfes, many=True).data

    return nfes_list

def get_nfe(id):
    nfes = NFE.objects.filter(id=id)
    nfe = nfe_serializer.FullNFeSerializer(nfes, many=True).data

    return nfe