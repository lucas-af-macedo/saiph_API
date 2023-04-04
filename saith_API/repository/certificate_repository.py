from ..models import Certificate, User_Certificate_Document

def get_certificate_with_code(code):
    certificate = Certificate.objects.filter(code=code)

    return certificate

def insert_certificate(certificate, password, expiration, document_id, code):
    certificate_result = Certificate.objects.create(certificate=certificate, password=password, expiration=expiration, document_id=document_id, code=code)

    return certificate_result.id

def insert_user_certificate_document(certificate_id, user_id, document_id):
    user_certificate = User_Certificate_Document.objects.create(certificate_id=certificate_id, user_id=user_id, document_id=document_id)

    return user_certificate.id

def update_user_certificate_document(user_certificate_document_id, certificate_id):
    User_Certificate_Document.objects.filter(id=user_certificate_document_id).update(certificate_id=certificate_id)

    return None

def get_user_certificate_document(user_id, document_id):
    user_certificate = User_Certificate_Document.objects.filter(user_id=user_id, document_id=document_id)

    return user_certificate