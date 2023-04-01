from ..models import Users, Teste
from django.core import serializers

def main(email):
    print(email)
    user = Users.objects.get(id=1)
    teste = user.teste.all()
    print(teste[0].oi)
    print('oi')
    print(user.teste)

    return user
