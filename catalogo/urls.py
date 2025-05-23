"""
URL configuration for catalogo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import (
    register_view, login_view, custom_logout, catalogo_view, home_view,
    painel_view, detalhes_produto, carrinho_view, editar_view,
    addcarrinho_view, remover_item_view, atualizar_item_view,
    obter_carrinho_view, finalizar_compra_view, lista_pedidos_view,
    detalhes_pedido_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('catalogo/', catalogo_view, name='catalogo'),
    path('home/', home_view, name='home'),
    path('', home_view, name='home'),
    path('painel/', painel_view, name='painel'),
    path('produto/<int:produto_id>/', detalhes_produto, name='detalhes'),
    path('carrinho/', carrinho_view, name='carrinho'),
    path('editar/', editar_view, name='editar'),
    path('addcarrinho/<int:produto_id>/adicionar/', addcarrinho_view, name='addcarrinho_view'),
    path('carrinho/remover/<int:produto_id>/', remover_item_view, name='remover_item'),
    path('carrinho/atualizar/<int:produto_id>/', atualizar_item_view, name='atualizar_item'),
    path('carrinho/obter/', obter_carrinho_view, name='obter_carrinho'),
    path('carrinho/finalizar/', finalizar_compra_view, name='finalizar_compra'),
    path('meus-pedidos/', lista_pedidos_view, name='lista_pedidos'),
    path('meus-pedidos/<int:pedido_id>/', detalhes_pedido_view, name='detalhes_pedido'),
]
