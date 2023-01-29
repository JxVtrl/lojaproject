from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Cliente, Categoria, Produto, Carro, CarroProduto, Pedido_order])