from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
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
        produto_id = self.kwargs['pro_id']
        produto_obj = Produto.objects.get(id=produto_id)
        carro_id = self.request.session.get("carro_id", None)
        if carro_id:
            carro_obj = Carro.objects.get(id=carro_id)
            produto_no_carro = carro_obj.carroproduto_set.filter(produto=produto_obj)
            if produto_no_carro.exists():
                carroproduto = produto_no_carro.last()
                carroproduto.quantidade += 1
                carroproduto.sub_total += produto_obj.venda
                carroproduto.save()
                carro_obj.total += produto_obj.venda
                carro_obj.save()

            else:
                carroproduto = CarroProduto.objects.create(carro=carro_obj, produto=produto_obj, avaliacao_produto=produto_obj.venda, quantidade=1, sub_total=produto_obj.venda)
                carro_obj.total += produto_obj.venda
                carro_obj.save()
        
        else:
            carro_obj = Carro.objects.create(total=0)
            self.request.session['carro_id'] = carro_obj.id
            carroproduto = CarroProduto.objects.create(carro=carro_obj, produto=produto_obj, avaliacao_produto=produto_obj.venda, quantidade=1, sub_total=produto_obj.venda)
            carro_obj.total += produto_obj.venda
            carro_obj.save()
        return context


class ManipularCarroView(View):
    def get(self, request, *args,  **kwargs):
        cp_id = self.kwargs["cp_id"]
        acao = request.GET.get("acao")
        cp_obj = CarroProduto.objects.get(id=cp_id)
        carro_obj = cp_obj.carro

        if acao == "inc":
            cp_obj.quantidade += 1
            cp_obj.sub_total += cp_obj.avaliacao_produto
            cp_obj.save()
            carro_obj.total += cp_obj.avaliacao_produto
            carro_obj.save()
        elif acao == "dcr":
            cp_obj.quantidade -= 1
            cp_obj.sub_total -= cp_obj.avaliacao_produto
            cp_obj.save()
            carro_obj.total -= cp_obj.avaliacao_produto
            carro_obj.save()

            if cp_obj.quantidade == 0:
                cp_obj.delete()

        elif acao == "rmv":
            carro_obj.total -= cp_obj.sub_total
            carro_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("lojaapp:meucarro")


class CheckoutView(TemplateView):
    template_name = "processar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carro_id = self.request.session.get("carro_id", None)
        if carro_id:
            carro = Carro.objects.get(id=carro_id)
        else:
            carro = None
        context['carro'] = carro
        return context


class LimparCarroView(View):
    def get(self, request, *args, **kwargs):
        carro_id = request.session.get("carro_id", None)
        if carro_id:
            carro = Carro.objects.get(id=carro_id)
            carro.carroproduto_set.all().delete()
            carro.total = 0
            carro.save()
        return redirect("lojaapp:meucarro")


class MeuCarroView(TemplateView):
    template_name = "meucarro.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carro_id = self.request.session.get("carro_id", None)
        if carro_id:
            carro = Carro.objects.get(id=carro_id)
        else:
            carro = None
        context['carro'] = carro
        return context

class SobreView(TemplateView):
    template_name = "sobre.html"

class ContatoView(TemplateView):
    template_name = "contato.html"

