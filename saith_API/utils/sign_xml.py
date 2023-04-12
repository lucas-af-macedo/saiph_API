import base64
from OpenSSL import crypto
from lxml import etree
import hashlib

def sign(pkcs12, xml):
    elements_list = find_id(xml)
    if not len(elements_list):
        elements_list.append(xml)

    signature, signed_info, signature_value_node, x509_certificate = signature_xml(elements_list)

    calcule_x509(pkcs12, x509_certificate)
    calcule_signature_value(pkcs12, signed_info, signature_value_node)

    return signature

def find_id(xml):
    elements_list = []
    attributes = xml.items()
    for attribute in attributes:
        if attribute[0] == 'Id':
            elements_list.append(xml)
    for element in xml:
        sub_element_list = find_id(element)
        for sub_element in sub_element_list:
            elements_list.append(sub_element)
    return elements_list


def calcule_x509(pkcs12, x509_certificate):
    cert = crypto.dump_certificate(crypto.FILETYPE_ASN1, pkcs12.get_certificate())

    x509 = base64.b64encode(cert).decode('utf-8')
    x509_certificate.text = x509

def calcule_digest_value(inf_evento, digest_value_node):
    root_canonicalizated =  etree.canonicalize(etree.tostring(inf_evento).decode())
    signed_data = root_canonicalizated.encode('UTF-8')

    digest_algorithm = 'sha1'
    digest = hashlib.new(digest_algorithm, signed_data).digest()
    
    digest_value = base64.b64encode(digest).decode('UTF-8')

    digest_value_node.text = digest_value

def calcule_signature_value(pkcs12, signed_info, signature_value_node):
    signed_info_canonicalized = etree.canonicalize(etree.tostring(signed_info).decode())
    xml_bytes = signed_info_canonicalized.encode("UTF-8")

    signature_algorithm = 'sha1'
    hash_signed_data = crypto.sign(pkcs12.get_privatekey(), xml_bytes, signature_algorithm)
    signature_value = base64.b64encode(hash_signed_data).decode('UTF-8')

    signature_value_node.text = signature_value

def signature_xml(elements_list):

    NSMAP = {None: 'http://www.w3.org/2000/09/xmldsig#'}

    signature = etree.Element('{http://www.w3.org/2000/09/xmldsig#}Signature', nsmap=NSMAP)

    signed_info = etree.SubElement(signature, '{http://www.w3.org/2000/09/xmldsig#}SignedInfo')

    canonicalization_method = etree.SubElement(signed_info, 'CanonicalizationMethod')
    canonicalization_method.set('Algorithm', 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315')
    signature_method = etree.SubElement(signed_info, 'SignatureMethod')
    signature_method.set('Algorithm', 'http://www.w3.org/2000/09/xmldsig#rsa-sha1')
    for node in elements_list:
        id = ''
        for attribute in node.items():
            if attribute[0] == 'Id':
                id = '#' + attribute[1]
        reference_node = etree.SubElement(signed_info, 'Reference')
        reference_node.set('URI', id)
        
        transforms_node = etree.SubElement(reference_node, 'Transforms')

        transform1_node = etree.SubElement(transforms_node, 'Transform')
        transform1_node.set('Algorithm', 'http://www.w3.org/2000/09/xmldsig#enveloped-signature')
        transform2_node = etree.SubElement(transforms_node, 'Transform')
        transform2_node.set('Algorithm', 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315')

        digest_method_node = etree.SubElement(reference_node, 'DigestMethod')
        digest_method_node.set('Algorithm', 'http://www.w3.org/2000/09/xmldsig#sha1')
        digest_value_node = etree.SubElement(reference_node, 'DigestValue')

        calcule_digest_value(node, digest_value_node)

    signature_value_node =  etree.SubElement(signature, 'SignatureValue')
    key_info =  etree.SubElement(signature, 'KeyInfo')
    x509_data =  etree.SubElement(key_info, 'X509Data')
    x509_certificate =  etree.SubElement(x509_data, 'X509Certificate')

    return signature, signed_info, signature_value_node, x509_certificate
