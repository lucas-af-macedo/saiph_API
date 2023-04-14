from ..repository import certificate_repository, document_repository
from datetime import datetime, timezone
import OpenSSL.crypto
import base64

def insert_certificate(certificate, password, user_id):
    cert = get_certificate_data_or_fail(certificate, password)

    subject = cert.get_subject()
    expiration = datetime.strptime(cert.get_notAfter().decode(), '%Y%m%d%H%M%SZ')
    code = cert.get_serial_number()
    document_number = subject.commonName.split(':')[-1]
    uf = subject.stateOrProvinceName
    uf_number = get_uf_number(uf)

    verify_expiration(expiration)
    document_id = verify_document_exist(document_number) 

    certificate_result = certificate_repository.get_certificate_with_code(code)
    user_certificate = certificate_repository.get_user_certificate_document(user_id=user_id, document_id=document_id)

    if(len(certificate_result) and len(user_certificate)):
        raise ValueError('Certificate already registred for this user!')

    if (not len(certificate_result)):
        certificate_id = certificate_repository.insert_certificate(certificate=certificate, password=password, expiration=expiration, document_id=document_id, code=code, uf=uf_number)
    else:
        certificate_id = certificate_result[0].id    

    if(not len(user_certificate)):
        certificate_repository.insert_user_certificate_document(certificate_id=certificate_id, user_id=user_id, document_id=document_id)
    else:
        certificate_repository.update_user_certificate_document(user_certificate_document_id=user_certificate[0].id, certificate_id=certificate_id)

    user_document_valid = certificate_repository.get_user_document_valid(user_id=user_id, document_id=document_id)

    if not len(user_document_valid):
        certificate_repository.insert_user_document_valid(user_id=user_id, document_id=document_id)

    return None

def get_uf_number(uf):
    if uf == 'AC':
        return '12'
    elif uf == 'AL':
        return '27'
    elif uf == 'AM':
        return '13'
    elif uf == 'AP':
        return '16'
    elif uf == 'BA':
        return '29'
    elif uf == 'CE':
        return '23'
    elif uf == 'DF':
        return '53'
    elif uf == 'ES':
        return '32'
    elif uf == 'GO':
        return '52'
    elif uf == 'MA':
        return '21'
    elif uf == 'MG':
        return '31'
    elif uf == 'MS':
        return '50'
    elif uf == 'MT':
        return '51'
    elif uf == 'PA':
        return '15'
    elif uf == 'PB':
        return '25'
    elif uf == 'PE':
        return '26'
    elif uf == 'PI':
        return '22'
    elif uf == 'PR':
        return '41'
    elif uf == 'RJ':
        return '33'
    elif uf == 'RN':
        return '24'
    elif uf == 'RO':
        return '11'
    elif uf == 'RR':
        return '14'
    elif uf == 'RS':
        return '43'
    elif uf == 'SC':
        return '42'
    elif uf == 'SE':
        return '28'
    elif uf == 'SP':
        return '35'
    elif uf == 'TO':
        return '17'
    else:
        return '91'


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