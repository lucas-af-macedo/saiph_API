from ..repository import nfe_repository, certificate_repository, document_repository
from datetime import datetime, timezone
from ..utils import soap_request
import pytz 
from ..models import NFE


def get_nfes(user_id, user_documento_valid_id):
    user_document = get_user_document_valid_or_fail(user_documento_valid_id, user_id)
    certificate = get_certificate_by_user_and_document_or_fail(user_id, user_document['document_id'])
    document, less_one_hour = get_document_or_fail(user_document)
    if not less_one_hour:
        get_nfes_from_sefaz(certificate, document)
    list_nfes = nfe_repository.get_nfes(document['id'])
    if not user_document['is_valid']:
        document_repository.update_user_document_valid(user_document['id'])
        
    return list_nfes

def get_nfe(user_id, nfe_id):
    nfe = nfe_repository.get_nfe(nfe_id)
    user_document = get_user_document_valid_or_fail(user_id)

def get_user_document_valid_or_fail(user_documento_valid_id, user_id):
    user_document = nfe_repository.get_user_document_valid(user_documento_valid_id, user_id)
    if not len(user_document):
        raise ValueError('Document doesnt exist or user dont has access')
    return user_document[0]

def get_certificate_by_user_and_document_or_fail(user_id, document_id):
    user_document = certificate_repository.get_user_certificate_document(user_id=user_id, document_id=document_id)
    certificate = certificate_repository.get_certificate_by_id(user_document[0].certificate_id)
    expiration = certificate.expiration
    expiration = expiration.astimezone(pytz.utc).replace(tzinfo=None)
    expired = verify_expiration(expiration)
    if expired:
        certificate_repository.update_certificate_invalid(certificate.id)
        raise ValueError('Certificate expired!')
    if not certificate.is_valid:
        raise ValueError('Certificate invalid!')
    
    return certificate

def get_document_or_fail(user_document):
    document = document_repository.get_document_by_id(user_document['document_id'])
    if user_document['is_valid']:
        date_format = '%Y-%m-%dT%H:%M:%S'
        last_request = document['last_request_nfe'][:-1].split('.')[0]
        date = datetime.strptime(last_request, date_format)
        less_one_hour = verify_last_request(date)
        if less_one_hour:
            return document, less_one_hour
    return document, False

def get_nfes_from_sefaz(certificate, document):
    while True:
        response_data = soap_request.post_distribuicao_dfe(certificate, document['last_nsu'], document['document_number'], certificate.uf, 'last_NSU')
        status = response_data['status']
        data = response_data['data']
        ult_nsu = data['ult_NSU']
        max_nsu = data['max_NSU']
        list_nfe = data['list_nfe']
        time = datetime.now()
        if status[:-1] == '28' or status == '473' or status == '':
            certificate_repository.update_certificate_invalid(certificate.id)
            raise ValueError('Certificate invalid!')
        if status == '137' or status == '656':
            document_repository.update_document_time(id=document['id'], time=time)
            return None
        list_nfe_to_insert = []
        for nfe in list_nfe:
            string_date = nfe['date_emit'][:-3] + nfe['date_emit'][-2:]
            date = datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%S%z')
            list_nfe_to_insert.append(NFE(nsu=nfe['NSU'], 
                seller=nfe['name'],
                number=nfe['nfe_number'],
                value_nfe=nfe['value_nfe'],
                date=date,
                has_nfe_complete=not nfe['resume_nfe'],
                nfe=nfe['xml'].encode('UTF-8'),
                document_id=document['id'],
                document_seller=nfe['CNPJ']))
        nfe_repository.insert_many_nfes(list_nfe_to_insert)
        if ult_nsu == max_nsu:
            document_repository.update_document(id=document['id'], ult_nsu=ult_nsu, time=time)
            return None
        document_repository.update_document_nsu(id=document['id'], ult_nsu=ult_nsu)
        return None

def verify_expiration(expiration):
    now = datetime.today()
    expired = expiration - now
    
    if (expired.total_seconds() < 0):
        return True
    return False
    
def verify_last_request(date):
    now = datetime.today()
    result = now - date
    print(result.total_seconds())
    
    if (result.total_seconds() < 3600):
        return True
    return False




    #if not user_document[0]['is_valid']:
       # raise ValueError('The certificate is invalid')