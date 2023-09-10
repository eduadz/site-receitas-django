from django.shortcuts import render, redirect
from django.http import Http404
from authors.forms import loginForm, RegisterForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout #aut checa se o usuario vai ou nao autenticar e login de fato loga no sistema   
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from authors.forms import AuthorRecipeForm

# Create your views here.
def register_view(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('authors:register_create'),
    })

def register_create(request):
    
    if not request.POST:
        raise Http404()
    
    
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    #adicionando os dados na base de dados:
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password) #salvando corretamente a senha na base de dados (criptografia)
        user.save()
        messages.success(request, 'Your user is created, please log in')

        #apagando dados da sessao
        del(request.session['register_form_data'])

    return redirect ('authors:login')

def login_view(request):
    form = loginForm()
    return render(request, 'authors/pages/login.html', context={
        'form': form,
        'form_action': reverse('authors:login_create'),

    })

def login_create(request):
    if not request.POST:
        raise Http404()

    form = loginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username = form.cleaned_data.get('username', ''),
            password = form.cleaned_data.get('password', '')
        )
        if authenticated_user is not None:
            messages.success(request, 'Logged in sucessfully')
            login(request, authenticated_user)
        
    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published = False,
        author = request.user,
    )
    return render(request, 'authors/pages/dashboard.html', context= {
        'recipes': recipes
    })

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published = False,
        author = request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()
    
    form = AuthorRecipeForm(
        data = request.POST or None, 
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        #agora form é valido e posso tentar salvar
        recipe = form.save(commit=False) #salva o formulario em recipe
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False 

        recipe.save() #salvando na base de dados
        messages.success(request, 'Sua receita foi salva com sucesso')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(request, 'authors/pages/dashboard_recipe.html', context= {
        'form': form,
    })

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_new(request):

    form = AuthorRecipeForm(        
        data = request.POST or None, # é usado para passar os dados recebidos de uma solicitação HTTP para o formulário
        files=request.FILES or None, #é usado para passar os arquivos enviados pelo usuário
    )

    if form.is_valid():
        recipe = form.save(commit=False) #salva o formulario em recipe
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False 

        recipe.save() #salvando na base de dados
        messages.success(request, 'Sua receita foi criada com sucesso')
        return redirect(reverse('authors:dashboard'))

    return render(request, 'authors/pages/dashboard_recipe_new.html', context= {
        'form': form,
    })  

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()
    
    #a pessoa nao entra diretamente no link 
    POST = request.POST
    id = POST.get('id') 
    
    recipe = Recipe.objects.filter(
        is_published = False,
        author = request.user,
        pk=id,
        
    ).first()

    if not recipe:
        raise Http404()
    
    recipe.delete()
    messages.success(request,'Deleted sucessfully.')
    return redirect(reverse('authors:dashboard'))
