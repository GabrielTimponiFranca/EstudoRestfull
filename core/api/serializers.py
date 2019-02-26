from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from core.models import PontoTuristico, Atracao, DocIdentificacao
from atracoes.api.serializers import AtracaoSerializer
from endereco.api.serializers import EnderecosSerializer
from endereco.models import Enderecos 


class DocIdentificacaoSerializer(ModelSerializer):
    class Meta:
        model = DocIdentificacao
        fields = '__all__'


class PontoTuristicoSerializer(ModelSerializer):
    atracoes = AtracaoSerializer(many=True, read_only=True)
    endereco = EnderecosSerializer(read_only=True)
    descricao_completa = SerializerMethodField()
    doc_identificacao = DocIdentificacaoSerializer()

    class Meta:
        model = PontoTuristico
        fields = (
            'id', 'nome', 'descricao', 'aprovado', 'foto',
            'atracoes', 'comentarios', 'avaliacao', 'endereco',
            'descricao_completa', 'descricao_completa2', 'doc_identificacao'
            )
        read_only_fields = ('comentarios', 'avaliacao')

   

    def get_descricao_completa(self, obj):
        return '%s - %s' % (obj.nome, obj.descricao)

    def create(self, validated_data):
        atracoes = validated_data['atracoes']
        del validated_data['atracoes']

        endereco = validated_data['endereco']
        del validated_data['endereco']
        end = Enderecos.objects.create(**endereco)

        doc = validated_data['doc_identificacao']
        del validated_data['doc_identificacao']
        doci = DocIdentificacao.objects.create(**doc)

        ponto = PontoTuristico.objects.create(**validated_data)
        self.cria_atracoes(atracoes, ponto)


        ponto.endereco = end
        ponto.doc_identificacao = doci

        ponto.save()

        return ponto
