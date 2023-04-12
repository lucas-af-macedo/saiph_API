from ..repository import certificate_repository, document_repository
from datetime import datetime, timezone
import OpenSSL.crypto
import base64

def insert_certificate(certificate, password, user_id=1):
    cert = get_certificate_data_or_fail(certificate, password)

    subject = cert.get_subject()
    expiration = datetime.strptime(cert.get_notAfter().decode(), '%Y%m%d%H%M%SZ')
    code = cert.get_serial_number()
    document_number = subject.commonName.split(':')[-1]

    verify_expiration(expiration)
    document_id = verify_document_exist(document_number) 

    certificate_result = certificate_repository.get_certificate_with_code(code)
    user_certificate = certificate_repository.get_user_certificate_document(user_id=user_id, document_id=document_id)

    if(len(certificate_result) and len(user_certificate)):
        raise ValueError('Certificate already registred for this user!')

    if (not len(certificate_result)):
        certificate_id = certificate_repository.insert_certificate(certificate=certificate, password=password, expiration=expiration, document_id=document_id, code=code)
    else:
        certificate_id = certificate_result[0].id    

    if(not len(user_certificate)):
        certificate_repository.insert_user_certificate_document(certificate_id=certificate_id, user_id=user_id, document_id=document_id)
    else:
        certificate_repository.update_user_certificate_document(user_certificate_document_id=user_certificate[0].id, certificate_id=certificate_id)

    return None







def get_certificate_data_or_fail(certificate, password):
    try:
        pfx = OpenSSL.crypto.load_pkcs12(certificate, password)
    except:
        raise ValueError('The password of certificate dont match')
    
    return pfx.get_certificate()


def verify_expiration(expiration):
    now = datetime.today()
    expired = expiration - now

    if (expired.total_seconds() < 0):
        raise ValueError('Certificate has expired!')
    
    return None

def verify_document_exist(document_number):
    document = document_repository.get_document(document_number)

    if (not len(document)):
        document_id = document_repository.insert_document(document_number)
    else:
        document_id = document[0].id

    return document_id