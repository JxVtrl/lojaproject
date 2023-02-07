from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo


class Categoria(models.Model):
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)

    def __str__(self):
        return self.titulo

class Produto(models.Model):
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to="produtos")
    preco_mercado = models.PositiveIntegerField()
    venda = models.PositiveIntegerField()
    descricao = models.TextField()
    garantia = models.CharField(max_length=100, null=True, blank=True)
    return_devolucao = models.CharField(max_length=300, null=True, blank=True)
    visualizacao = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

class Carro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    criado_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Carro" + str(self.id)

class CarroProduto(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    avaliacao_produto = models.PositiveIntegerField()
    quantidade = models.PositiveIntegerField()
    sub_total = models.PositiveIntegerField()

    def __str__(self):
        return "Carro" + str(self.carro.id) + "CarroProduto" + str(self.id)

PEDIDO_STATUS = (
    ("Pedido recebido", "Pedido recebido"),
    ("Pedido sendo processado", "Pedido sendo processado"),
    ("Pedido a caminho", "Pedido a caminho"),
    ("Pedido entregue", "Pedido entregue"),
    ("Pedido cancelado", "Pedido cancelado"),
)

class Pedido_order(models.Model):
    carro = models.OneToOneField(Carro, on_delete=models.CASCADE)
    ordenado_por = models.CharField(max_length=100)
    endereco_envio = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    endereco_envio = models.CharField(max_length=200)
    sub_total = models.PositiveIntegerField
    desconto = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    pedido_status = models.CharField(max_length=50, choices=PEDIDO_STATUS)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Pedido_order: " + str(self.id)