from lxml import etree
import os

def distribuicao_dfe(NSU, document_number, state_number, search_type):
    dist_dfe = dist_dfe_xml(NSU, document_number, state_number, search_type)

    soap_envelope = get_soap_event(dist_dfe)

    return soap_envelope

def get_soap_event(element):
    NSMAP = {
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xsd': "http://www.w3.org/2001/XMLSchema",
        'soap': 'http://schemas.xmlsoap.org/soap/envelope/'
    }
    
    soap_envelope = etree.Element('{http://schemas.xmlsoap.org/soap/envelope/}Envelope', nsmap=NSMAP)
    body = etree.SubElement(soap_envelope, '{http://schemas.xmlsoap.org/soap/envelope/}Body')
    nfe_dist_dfe = etree.SubElement(body, 'nfeDistDFeInteresse')
    nfe_dist_dfe.set('xmlns', "http://www.portalfiscal.inf.br/nfe/wsdl/NFeDistribuicaoDFe")
    nfe_data = etree.SubElement(nfe_dist_dfe, 'nfeDadosMsg')
    nfe_data.append(element)
    return soap_envelope

def dist_dfe_xml(NSU, document_number, state_number, search_type):
    dist_dfe = etree.Element('distDFeInt')
    dist_dfe.set('xmlns', "http://www.portalfiscal.inf.br/nfe")
    dist_dfe.set('versao', "1.01")

    tp_amb = etree.SubElement(dist_dfe, 'tpAmb')
    tp_amb.text = os.getenv('ENVIRONMENT_TYPE')
    uf_autor = etree.SubElement(dist_dfe, 'cUFAutor')
    uf_autor.text = state_number
    if len(document_number) == 11:
        document = etree.SubElement(dist_dfe, 'CPF')
    else:
        document = etree.SubElement(dist_dfe, 'CNPJ')
    document.text = document_number
    if search_type == 'last_NSU':
        dist_nsu = etree.SubElement(dist_dfe, 'distNSU')
        ult_nsu = etree.SubElement(dist_nsu, 'ultNSU')
        ult_nsu.text = NSU
    elif search_type == 'chave_nfe':
        cons_ch_nfe = etree.SubElement(dist_dfe, 'consChNFe')
        ch_nfe = etree.SubElement(cons_ch_nfe, 'chNFe')
        ch_nfe.text = NSU

    return dist_dfe