from .models import Aluguel, Casa
from rest_framework import serializers
from django.db.models import Q #criação de filtros para nosso db
from datetime import date #manipulação/comparação de datas


class CasaSerializer(serializers.ModelSerializer):

    #dono = serializers.PrimaryKeyRelatedField(read_only=True)
    dono = serializers.ReadOnlyField(source = 'dono.username')

    class Meta:
        model = Casa
        fields = ('id','dono', 'titulo', 'descricao', 'endereco', 'num_quartos', 'preco_dia', 'data_cadastro')
        read_only_fields = ('data_cadastro', 'id')

"""
        a pk é recebida na requisição do user que estiver logado no init de PrimaryKeyRelatedField
        casa = vai receber a pk do request.user autenticado pela view, recebe no parametro a lista de casas e verifica se o 'pk' recebido esta na lista de casas.
        Quando eu faço a requisição e passo os dados da casa que vou alugar o DRF-SERIALIZER:
        verifica se a cada de pk 'x' existe no meu banco, o hospede é da mesma forma, porém não é recebido na requisição, ele é capturado quando um user logado no sistema faz a requisição, o serializer após isso, pega os dados da requisição, e quando chamar o serializer.is_valid(), as funções de validate() é chamada, os campos são verificados, e os dados ali presentes são os candidatos a serem adicionados ao meu validated_data final, após isso os dados são populados no .save() ocorrendo assim a persistência  

        Q = formula para saber se duas faixas de tempo estão se cruzando, verifica se a entrada do user 'Mario' acontece antes da saida do User João
    """
class AluguelSerializer(serializers.ModelSerializer):
    casa = serializers.PrimaryKeyRelatedField(queryset=Casa.objects.all())
    hospede = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = Aluguel
        fields = ('id','casa', 'hospede', 'valor_aluguel', 'data_entrada','data_saida') 
        read_only_fields = ('id', 'valor_aluguel',) 

    def validate(self, data:dict) -> dict:
        casa_registrada = data.get('casa')
        data_entrada = data.get('data_entrada')
        data_saida = data.get('data_saida')
        
        if data_entrada and data_saida and data_entrada >= data_saida:
            raise serializers.ValidationError({"data_saida":"A data de saida tem que ser posterior a data de entrada."})
        
        if self.instance is None and data_entrada and data_entrada < date.today():
            raise serializers.ValidationError({"data_entrada":"A data de entrada não pode ser retroativa."})
        
        alugueis_da_casa = Aluguel.objects.filter(casa=casa_registrada) 
        if self.instance:
            alugueis_da_casa = alugueis_da_casa.exclude(pk=self.instance.pk)
        
        sobreposicao_de_alugueis = alugueis_da_casa.filter(
            Q(data_entrada__lt=data_saida, data_saida__gt=data_entrada)
        ).exists()

        if sobreposicao_de_alugueis:
            raise serializers.ValidationError({"error":"A data escolhida já está ocupada no momento."}) 
        
        if data_entrada and data_saida:
            periodo_alugado = data_saida - data_entrada
            num_dias = periodo_alugado.days
            data['valor_aluguel'] = num_dias * casa_registrada.preco_dia
            return data
        
        return data