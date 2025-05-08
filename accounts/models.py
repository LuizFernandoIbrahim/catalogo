from django.db import models

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