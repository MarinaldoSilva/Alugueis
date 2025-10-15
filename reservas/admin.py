from django.contrib import admin
from .models import Aluguel, Casa


@admin.register(Casa)
class CasaAdmin(admin.ModelAdmin):
    list_display = ('dono','endereco','num_quartos','preco_dia','data_cadastro') #campos de mostragem
    list_filter = ('dono','num_quartos','preco_dia') #campos de filtro
    search_fields = ('dono__username','endereco','descricao')#buscar informação por palavras
    date_hierarchy = 'data_cadastro'

@admin.register(Aluguel)
class AluguelAdmin(admin.ModelAdmin):
    list_display = ('casa', 'hospede', 'data_entrada', 'data_saida', 'valor_aluguel', 'datas_aluguel')
    list_filter = ('casa__titulo',)
    search_fields = ('data_entrada','data_saida', 'casa__titulo')
    date_hierarchy = ('data_entrada')