from rest_framework.viewsets import ModelViewSet
from endereco.models import Enderecos
from .serializers import EnderecosSerializer


class EnderecosViewSet(ModelViewSet):
    queryset = Enderecos.objects.all()
    serializer_class = EnderecosSerializer
