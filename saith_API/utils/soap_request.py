from OpenSSL import crypto
import os
from lxml import etree
from requests_pkcs12 import post
from io import BytesIO
from .recepcao_evento import recepcao_evento
from .distribuicao_dfe import distribuicao_dfe
import urllib3
from .nfe_data import get_response_data
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def post_recepcao_evento(certificate, type_event, key_nfe, lote, document_number, state_number, justification=''):
    pkcs12, pkcs12_data, pkcs12_password = load_pkcs12(certificate)
    soap_envelope = recepcao_evento(pkcs12, type_event, key_nfe, lote, document_number, state_number, justification)

    body = etree.tostring(soap_envelope, xml_declaration=True, encoding='UTF-8')
    environment = os.getenv('ENVIRONMENT_TYPE')
    if environment == '2':
        url = "https://hom1.nfe.fazenda.gov.br/NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx"
    elif environment == '1':
        url = "https://www.nfe.fazenda.gov.br/NFeRecepcaoEvento4/NFeRecepcaoEvento4.asmx"
    headers = {'content-type': 'text/xml'}
    try:
        response = post(url, data=body, headers=headers, pkcs12_data=pkcs12_data, pkcs12_password=pkcs12_password, verify=False)
    except ValueError as err:
        return {'status': '', 'text': '', 'error': err}
    data_bytes = BytesIO(response.content)
    root = etree.parse(data_bytes).getroot()
    status = root.findall(".//{http://www.portalfiscal.inf.br/nfe}cStat")[-1].text
    status_text = root.findall(".//{http://www.portalfiscal.inf.br/nfe}xMotivo")[-1].text

    return {'status': status, 'text':status_text, 'error': ''}

def post_distribuicao_dfe(certificate, NSU, document_number, state_number, search_type):
    pkcs12, pkcs12_data, pkcs12_password = load_pkcs12(certificate)

    soap_envelope = distribuicao_dfe(NSU, document_number, state_number, search_type)
    body = etree.tostring(soap_envelope, xml_declaration=True, encoding='UTF-8')

    environment = os.getenv('ENVIRONMENT_TYPE')
    if environment == '2':
        url = "https://hom1.nfe.fazenda.gov.br/NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx"
    elif environment == '1':
        url = "https://www1.nfe.fazenda.gov.br/NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx"
    headers = {'content-type': 'text/xml'}
    """try:
        response = post(url, data=body, headers=headers, pkcs12_data=pkcs12_data, pkcs12_password=pkcs12_password, verify=False)
    except ValueError as err:
        return {'status': '', 'text': '', 'data': '', 'error': err}"""
    content = open('response38.xml', 'rb').read()
    data_bytes = BytesIO(content)
    root = etree.parse(data_bytes).getroot()
    data = get_response_data(root)
    status = root.findall(".//{http://www.portalfiscal.inf.br/nfe}cStat")[-1].text
    status_text = root.findall(".//{http://www.portalfiscal.inf.br/nfe}xMotivo")[-1].text
    date = root.find(".//{http://www.portalfiscal.inf.br/nfe}dhResp").text
    #file = open('responses/%s.xml'%date, 'wb')
    #file.write(response.content)
    #file.close()
    return {'status': status, 'text': status_text, 'data': data, 'error': ''}

def load_pkcs12(certificate):
    pkcs12_data = bytes(certificate.certificate)
    pkcs12_password = certificate.password
    pkcs12 = crypto.load_pkcs12(pkcs12_data, pkcs12_password)
    return pkcs12, pkcs12_data, pkcs12_password