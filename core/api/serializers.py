from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from core.models import PontoTuristico, Atracao
from atracoes.api.serializers import AtracaoSerializer
from endereco.api.serializers import EnderecosSerializer


class PontoTuristicoSerializer(ModelSerializer):
    atracoes = AtracaoSerializer(many=True, read_only=True)
    endereco = EnderecosSerializer(read_only=True)
    descricao_completa = SerializerMethodField()

    class Meta:
        model = PontoTuristico
        fields = (
            'id', 'nome', 'descricao', 'aprovado', 'foto',
            'atracoes', 'comentarios', 'avaliacao', 'endereco',
            'descricao_completa', 'descricao_completa2'
            )
        read_only_fields = ('comentarios', 'avaliacao')

   

    def get_descricao_completa(self, obj):
        return '%s - %s' % (obj.nome, obj.descricao)
        