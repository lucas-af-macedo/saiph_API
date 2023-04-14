from ..utils import soap_request
from ..models import Certificate

def test(oi):
    certificate = Certificate.objects.get(id=10)

    #dados da nota fiscal
    key_nfe = '33230100074569004008550100003443571310472362'
    key_nfe = '33221262461140002915550550031922381808393903'
    
    #dados da empresa
    lote = '000000000000002'
    document_number = certificate.document.document
    state_number = '33'
    
    #dados da escolha do usuario
    type_event = '210210'
    justification = ''

    #response_data = soap_request.post_recepcao_evento(certificate, type_event, key_nfe, lote, document_number, state_number, justification)
    response_data = soap_request.post_distribuicao_dfe(certificate, key_nfe, document_number, state_number, 'chave_nfe')
    #response_data = teste.test()
    #print(response_data)
    print('ok')

    #280: "Rejeição: Certificado Transmissor inválido"

    #108: “Rejeição: Serviço Paralisado Momentaneamente (curto prazo)
    #109: “Rejeição: Serviço Paralisado sem previsão”