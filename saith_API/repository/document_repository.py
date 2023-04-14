from ..models import Document, User_Document_Valid

def get_document(document_number):
    document = Document.objects.filter(document_number=document_number)

    return document

def insert_document(document_number, name, document_type):
    document = Document.objects.create(document_number=document_number, name=name, document_type=document_type)

    return document.id

def get_user_document_valid(user_id):
    document = User_Document_Valid.objects.filter(user_id=user_id)

    return document