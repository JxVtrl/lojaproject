from django.urls import path
from.views import *

app_name = "lojaapp"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("all-products/", TodosProdutosView.as_view(), name="allproducts"),
    path("produto/<slug:slug>/", ProdutoDetalheView.as_view(), name="produtodetalhe"),
    path("addcarro-<int:pro_id>/", AddCarroView.as_view(), name="addcarro"),
    path("meu-carro/", MeuCarroView.as_view(), name="meucarro"),
    path("manipular-carro/<int:cp_id>/", ManipularCarroView.as_view(), name="manipularcarro"),
]