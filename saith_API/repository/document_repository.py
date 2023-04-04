from ..models import Document

def get_document(document_number):
    document = Document.objects.filter(document=document_number)

    return document

def insert_document(document_number):
    document = Document.objects.create(document=document_number)

    return document.id