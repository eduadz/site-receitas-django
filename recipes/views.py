from django.http import Http404 
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from django.core.paginator import Paginator


from utils.recipes.factory import make_recipe
from utils.recipes.pagination import make_pagination_range
from .models import Recipe

# Create your views here.

def home(request):
    recipes = Recipe.objects.filter(
        is_published = True
    ).order_by('-id')

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    
    #parte do paginator
    paginator = Paginator(recipes,2) #duas receitas por pagina
    page_obj = paginator.get_page(current_page)
    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )

    return render(request, 'recipes/pages/home.html', context={
        'recipes' : recipes,
        #'pagination_range': pagination_range
    })
#context adiciona dicionario aos templates
#utilizando looping para gerar 6 dados aleatórios dentro do dicionário recipes : [make_recipe() for _ in range(6)]

def category(request, category_id):
    recipes = Recipe.objects.filter(
        is_published = True,
        category__id = category_id #category__id acessa a tabela category a partir da foreign key na tabela recipe em busca do id
    ).order_by('-id')

    if not recipes:
        raise Http404('Category not found')

    return render(request, 'recipes/pages/category.html', context={
        'recipes' : recipes,
        'title' : f'{recipes.first().category.nome} - Category |',
    })


def recipe(request, id):
    recipe = Recipe.objects.filter(
        is_published = True,
        id = id 
    ).order_by('-id').first()

    #outra maneira de fazer sem ser consulta a mão: utilizando django shortcuts
    #recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe' : recipe,
        'is_detail_page': True,                                                                      
    })

def search(request):
    #pegando termo do input no html
    search_term = request.GET.get('q', '').strip() 

    if not search_term:
        raise Http404()
    
    #mostrar receitas baseadas no search_term
    recipes = Recipe.objects.filter(
        Q(title__icontains = search_term) | Q(description__icontains = search_term),
        is_published = True,
    ).order_by('-id')
    
    
    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for {search_term}',
        'recipes':recipes,
    })

