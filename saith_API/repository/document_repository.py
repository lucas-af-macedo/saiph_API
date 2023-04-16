from ..models import Document, User_Document_Valid
from ..serializers.document_serializer import DocumentOnlyIdAndDocument, FullDocumentSerializer

def get_document(document_number):
    document = Document.objects.filter(document_number=document_number)

    return document

def insert_document(document_number, name, document_type):
    document = Document.objects.create(document_number=document_number, name=name, document_type=document_type)

    return document.id

def get_document_by_id(id):
    documents = Document.objects.filter(id=id)
    document =  FullDocumentSerializer(documents, many=True).data[0]

    return document

def get_user_document_valid(user_id):
    document = User_Document_Valid.objects.filter(user_id=user_id)
    documents_list =  DocumentOnlyIdAndDocument(document, many=True).data

    return documents_list

def update_document_nsu(id, ult_nsu):
    Document.objects.filter(id=id).update(last_nsu=ult_nsu)

    return None

def update_document_time(id, time):
    Document.objects.filter(id=id).update(last_request_nfe=time)

    return None

def update_document(id, ult_nsu, time):
    Document.objects.filter(id=id).update(last_nsu=ult_nsu, last_request_nfe=time)

    return None

def update_user_document_valid(id):
    User_Document_Valid.objects.filter(id=id).update(is_valid=True)

    return None