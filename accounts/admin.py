from django.contrib import admin
from .models import Produto, ItemPedido, Pedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    fields = ('produto', 'nome_produto', 'preco_item', 'quantidade', 'get_subtotal')
    readonly_fields = ('nome_produto', 'preco_item', 'get_subtotal') # Campos calculados ou copiados
    extra = 0 # Não mostrar linhas extras para adicionar

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'data_pedido', 'valor_total', 'status')
    list_filter = ('status', 'data_pedido', 'usuario')
    search_fields = ('id', 'usuario__username', 'usuario__email')
    readonly_fields = ('usuario', 'data_pedido', 'valor_total') # Campos definidos na criação
    list_editable = ('status',) # Permite editar o status na lista (opcional)
    inlines = [ItemPedidoInline] # Mostra os itens relacionados dentro do pedido

    fieldsets = (
        (None, {
            'fields': ('usuario', 'data_pedido', 'valor_total')
        }),
        ('Status e Entrega', {
            'fields': ('status',) # Adicione 'endereco_entrega', 'codigo_rastreio' se os criar no model
        }),
    )
# Registro simples para Produto (como você já tinha)
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
     list_display = ('nome', 'preco', 'categoria', 'is_active')
     list_filter = ('categoria', 'is_active')
     search_fields = ('nome', 'descricao')