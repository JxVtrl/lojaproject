from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *

class HomeView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produto_list'] = Produto.objects.all()
        return context

class TodosProdutosView(TemplateView):
    template_name = "todosprodutos.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todascategorias'] = Categoria.objects.all().order_by('-id')
        return context    

class ProdutoDetalheView(TemplateView):
    template_name = "produtodetalhe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = kwargs['slug']
        produto = Produto.objects.get(slug=url_slug)
        produto.visualizacao += 1
        produto.save()
        context['produto'] = produto
        return context

class AddCarroView(TemplateView):
    template_name = "addprocarro.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto_id = kwargs['pro_id']
        produto_obj = Produto.objects.get(id=produto_id)
        carro_id = self.request.session.get("carro_id", None)
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
        else:
            carro_obj = Carro.objects.create(total=0)
            self.request.session['carro_id'] = carro_obj.id

class SobreView(TemplateView):
    template_name = "sobre.html"

class ContatoView(TemplateView):
    template_name = "contato.html"

    