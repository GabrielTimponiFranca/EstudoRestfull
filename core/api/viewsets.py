from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from core.models import PontoTuristico
from .serializers import PontoTuristicoSerializer


class PontoTuristicoViewSet (ModelViewSet):
    queryset = PontoTuristico.objects.all()
    serializer_class = PontoTuristicoSerializer
    filter_backends = (SearchFilter, )
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    search_fields = ('nome', 'descricao', 'endereco__linha1')
    
    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        nome = self.request.query_params.get('nome', None)
        descricao = self.request.query_params.get('descricao', None)
        queryset = PontoTuristico.objects.all()
        if id:
            queryset = queryset.objects.filter(id=id)

        if nome:
            queryset = queryset.objects.filter(nome_iexact=nome) 

        if descricao:
            queryset = queryset.objects.filter(descricao_iexact=descricao)
        return queryset

    @action(methods=('post', 'get'), detail=True)
    def denunciar(self, request, pk=None):
        pass

    @action(methods=('get'), detail=False)
    def teste(self, request):
        pass

    @action(methods=['post'], detail=True)
    def associa_atracoes(self, request, id):
        atracoes = request.data['ids']

        ponto = PontoTuristico.objects.get(id=id)

        ponto.atracoes.set(atracoes)

        ponto.save()
        return HttpResponse('Ok')
