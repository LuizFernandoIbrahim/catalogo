from django.db import models
from django.conf import settings

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # Armazena preços (ex: 199.99)
    imagem = models.URLField()  # Armazena a URL da imagem
    categoria = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)  # Permite descrições em branco
    is_active = models.BooleanField(default=True)
    # Outros campos que você possa precisar

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    # Vínculo com o usuário que fez o pedido
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    # Data e hora que o pedido foi criado
    data_pedido = models.DateTimeField(auto_now_add=True)
    # Valor total calculado no momento da finalização
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Campo para informações adicionais, como endereço (opcional)
    # endereco_entrega = models.TextField(null=True, blank=True)
    # codigo_rastreio = models.CharField(max_length=50, null=True, blank=True)

    # --- Campo de Status ---
    STATUS_AGUARDANDO_PAGAMENTO = 'aguardando_pagamento'
    STATUS_PROCESSANDO = 'processando'
    STATUS_ENVIADO = 'enviado'
    STATUS_ENTREGUE = 'entregue'
    STATUS_CANCELADO = 'cancelado'

    STATUS_CHOICES = [
        (STATUS_AGUARDANDO_PAGAMENTO, 'Aguardando Pagamento'),
        (STATUS_PROCESSANDO, 'Em Processamento'),
        (STATUS_ENVIADO, 'Enviado'),
        (STATUS_ENTREGUE, 'Entregue'),
        (STATUS_CANCELADO, 'Cancelado'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AGUARDANDO_PAGAMENTO # Status inicial padrão
    )

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username if self.usuario else 'Usuário Anônimo'}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_pedido'] # Ordenar por mais recente

class ItemPedido(models.Model):
    # Vínculo com o Pedido ao qual este item pertence
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    # Vínculo com o Produto que foi comprado
    # Usamos SET_NULL para caso o produto seja excluído, o item ainda exista no histórico do pedido
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    # Guarda o nome e preço no momento da compra (caso o produto original mude)
    nome_produto = models.CharField(max_length=255)
    preco_item = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.nome_produto} (Pedido #{self.pedido.id})"

    def get_subtotal(self):
        return self.preco_item * self.quantidade

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens dos Pedidos"