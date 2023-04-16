from ..repository import document_repository

def get_documents(user_id):
    documents = document_repository.get_user_document_valid(user_id)
    
    return documents