from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Produto
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@login_required
@user_passes_test(lambda user: user.is_superuser)
def adicionar_produto_view(request):
    try:
        data = json.loads(request.body)
        produto = Produto.objects.create(
            nome=data["nome"],
            preco=data["preco"],
            imagem=data["imagem"],
            categoria=data["categoria"],
            descricao=data.get("descricao", ""),
            is_active=True
        )
        return JsonResponse({"sucesso": True})
    except Exception as e:
        return JsonResponse({"sucesso": False, "erro": str(e)})

def addcarrinho_view(request, produto_id):
    if request.method == "POST":
        quantidade = int(request.POST.get("quantidade", 1))
        produto = get_object_or_404(Produto, id=produto_id)

        # Adicionar ao carrinho (session)
        carrinho = request.session.get("carrinho", {})
        carrinho[str(produto_id)] = carrinho.get(str(produto_id), 0) + quantidade
        request.session["carrinho"] = carrinho

        return JsonResponse({"sucesso": True})

    return JsonResponse({"sucesso": False})

def detalhes_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'detalhes.html', {'produto': produto})

def register_view(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('catalogo')
        else:
            login_form = AuthenticationForm()
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form':login_form})

def custom_logout(request):
    logout(request)
    messages.success(request, "Você saiu com sucesso.")
    return redirect('home')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def painel_view(request):
    return render(request, 'painel.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def catalogo_view(request):
    produtos = Produto.objects.filter(is_active=True)  # Certifique-se de filtrar por produtos ativos
    categorias = Produto.objects.values_list('categoria', flat=True).distinct()
    return render(request, 'catalogo.html', {
        'produtos': produtos,
        'categorias': categorias,
    })

def home_view(request):
    return render(request, 'home.html')

def detalhes_view(request):
    return render(request, 'detalhes.html')

def editar_view(request):
    return render(request, 'editar.html')

@login_required
def carrinho_view(request):
    carrinho = request.session.get("carrinho", {})
    cart_items = []
    total = 0

    for produto_id, quantidade in carrinho.items():
        produto = Produto.objects.filter(id=produto_id).first()
        if produto:
            item_total = produto.preco * quantidade
            total += item_total
            cart_items.append({
                'id': produto.id,
                'nome': produto.nome,
                'image_url': produto.imagem if produto.imagem else '',
                'preco': f"{produto.preco:.2f}",
                'quantidade': quantidade,
                'subtotal': f"{item_total:.2f}",
            })

    context = {
        'cart_items': cart_items,
        'total': f"{total:.2f}"
    }

    return render(request, 'carrinho.html', context)

@login_required
def obter_carrinho_view(request):
    carrinho = request.session.get("carrinho", {})
    itens = []

    for produto_id_str, quantidade in carrinho.items():
        try:
            produto = Produto.objects.get(id=produto_id_str)
            itens.append({
                "produto": {
                    "id": produto.id,
                    "nome": produto.nome,
                    # Verifique se a imagem existe antes de acessar a URL
                    "imagem": produto.imagem if produto.imagem and hasattr(produto.imagem, 'url') else "",
                    "preco": float(produto.preco),
                },
                "quantidade": quantidade
            })
        except Produto.DoesNotExist:
            continue

    return JsonResponse({
        "sucesso": True,
        "carrinho": {
            "itens": itens
        }
    })

@require_POST
@login_required
def remover_item_view(request, produto_id):
    carrinho = request.session.get("carrinho", {})
    produto_id_str = str(produto_id)
    if produto_id_str in carrinho:
        del carrinho[produto_id_str]
        request.session["carrinho"] = carrinho
    return redirect('carrinho')

@require_POST
@login_required
def atualizar_item_view(request, produto_id):
    quantidade = int(request.POST.get("quantidade", 1))
    if quantidade < 1:
        quantidade = 1

    carrinho = request.session.get("carrinho", {})
    carrinho[str(produto_id)] = quantidade
    request.session["carrinho"] = carrinho
    return redirect('carrinho')

@require_POST
@login_required
def finalizar_compra_view(request):
    carrinho = request.session.get("carrinho", {})

    if not carrinho:
        return JsonResponse({"sucesso": False, "erro": "Seu carrinho está vazio."})

    # Aqui você pode salvar o pedido no banco, enviar e-mail etc.

    # Limpar carrinho da sessão após finalizar
    request.session["carrinho"] = {}

    return JsonResponse({
        "sucesso": True,
        "mensagem": "Compra finalizada com sucesso.",
        "redirect": "/catalogo/"  # ou página de "Obrigado"
    })