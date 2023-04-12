from lxml import etree
import datetime
from .sign_xml import sign
import os


def recepcao_evento(pkcs12, type_event, key_nfe, lote, document_number, state_number, justification):
    inf_evento = event_xml(type_event, key_nfe, document_number, state_number, justification)
    signature = sign(pkcs12, inf_evento)

    env_evento = envelop_xml(inf_evento, signature, lote)
    soap_envelope = get_soap_event(env_evento)

    return soap_envelope


def get_soap_event(env_evento):
    NSMAP = {
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xsd': "http://www.w3.org/2001/XMLSchema",
        'soap': 'http://schemas.xmlsoap.org/soap/envelope/'
    }
    
    soap_envelope = etree.Element('{http://schemas.xmlsoap.org/soap/envelope/}Envelope', nsmap=NSMAP)
    body = etree.SubElement(soap_envelope, '{http://schemas.xmlsoap.org/soap/envelope/}Body')
    nfe_data = etree.SubElement(body, 'nfeDadosMsg')
    nfe_data.set('xmlns', "http://www.portalfiscal.inf.br/nfe/wsdl/NFeRecepcaoEvento4")
    nfe_data.append(env_evento)
    return soap_envelope


def envelop_xml(inf_evento, signature, lote):

    NSMAP = {None: 'http://www.portalfiscal.inf.br/nfe'}
    
    env_evento = etree.Element('{http://www.portalfiscal.inf.br/nfe}envEvento', nsmap=NSMAP)
    env_evento.set('versao', '1.00')

    id_lote = etree.SubElement(env_evento, '{http://www.portalfiscal.inf.br/nfe}idLote')    
    id_lote.text = lote
    evento = etree.SubElement(env_evento, '{http://www.portalfiscal.inf.br/nfe}evento')
    evento.set('versao', '1.00')

    evento.append(inf_evento)
    evento.append(signature)

    return env_evento



def event_xml(type_event, key_nfe, document_number, state_number, justification):

    timezone = datetime.timezone(datetime.timedelta(hours=-3), 'America/Sao_Paulo')
    now = datetime.datetime.now(timezone)
    offset = now.strftime('%z')
    time_now = now.strftime('%Y-%m-%dT%H:%M:%S')+offset[:-2]+':'+offset[-2:]

    id = 'ID' + type_event + key_nfe + '01'

    inf_evento = etree.Element("{http://www.portalfiscal.inf.br/nfe}infEvento", nsmap={None: 'http://www.portalfiscal.inf.br/nfe'})
    inf_evento.set('Id', id)
    
    c_orgao = etree.SubElement(inf_evento, 'cOrgao')
    c_orgao.text = state_number
    tp_amb = etree.SubElement(inf_evento, 'tpAmb')
    tp_amb.text = os.getenv('ENVIRONMENT_TYPE')
    if len(document_number) == 14:
        cnpj = etree.SubElement(inf_evento, 'CNPJ')
        cnpj.text = document_number
    elif len(document_number) == 11:
        cpf = etree.SubElement(inf_evento, 'CPF')
        cpf.text = document_number
    ch_nfe = etree.SubElement(inf_evento, 'chNFe')
    ch_nfe.text = key_nfe
    dh_evento = etree.SubElement(inf_evento, 'dhEvento')
    dh_evento.text = time_now
    tp_evento = etree.SubElement(inf_evento, 'tpEvento')
    tp_evento.text = type_event
    n_seq_evento = etree.SubElement(inf_evento, 'nSeqEvento')
    n_seq_evento.text = '1'
    ver_evento = etree.SubElement(inf_evento, 'verEvento')
    ver_evento.text = '1.00'
    det_evento = etree.SubElement(inf_evento, 'detEvento')
    det_evento.set('versao', '1.00')

    desc_evento = etree.SubElement(det_evento, 'descEvento')
    if type_event == '210200':
        desc_evento.text = 'Confirmacao da Operacao'
    elif type_event == '210210':
        desc_evento.text = 'Ciencia da Operacao'
    elif type_event == '210220':
        desc_evento.text = 'Desconhecimento da Operacao'
    elif type_event == '210240':
        desc_evento.text = 'Operacao nao Realizada'
        x_just = etree.SubElement(det_evento, 'xJust')
        x_just.text = justification

    return inf_evento
