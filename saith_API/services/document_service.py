from ..repository import document_repository
from ..serializers.document_serializer import DocumentOnlyIdAndDocument

def get_documents(user_id):
    documents = document_repository.get_user_document_valid(user_id)
    if not len(documents):
        raise ValueError('No documents found!')
    document_list = []
    for document in documents:
        document_list.append(DocumentOnlyIdAndDocument(document.document).data)
    return document_list