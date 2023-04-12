import zlib
from io import BytesIO
from lxml import etree
import base64

def get_response_data(root):
    elements = root.findall(".//{http://www.portalfiscal.inf.br/nfe}docZip")
    list_data = []
    for element in elements:
        attributes = element.items()
        if 'resNFe' in attributes[1][1]:
            arq_compressed = base64.b64decode(element.text)
            xml = zlib.decompress(arq_compressed, 16 + zlib.MAX_WBITS)
            element_root = etree.parse(BytesIO(xml)).getroot()
            nfe_number = element_root.find(".//{http://www.portalfiscal.inf.br/nfe}chNFe").text
            cnpj = element_root.find(".//{http://www.portalfiscal.inf.br/nfe}CNPJ").text
            name = element_root.find(".//{http://www.portalfiscal.inf.br/nfe}xNome").text
            value_nfe = element_root.find(".//{http://www.portalfiscal.inf.br/nfe}vNF").text
            date_emit = element_root.find(".//{http://www.portalfiscal.inf.br/nfe}dhEmi").text
            list_data.append({'NSU': attributes[0][1], 'nfe_number': nfe_number, 'CNPJ': cnpj,'name': name, 'value_nfe': value_nfe, 'date_emit': date_emit, 'resume_nfe': True, 'xml': xml.decode('utf-8')})
    ult_nsu = root.find(".//{http://www.portalfiscal.inf.br/nfe}ultNSU")
    if ult_nsu == None:
        response_data = {}
    else:
        response_data = {'ultNSU': ult_nsu.text, 'list_nfe': list_data}
    return response_data