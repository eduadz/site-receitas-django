from django.http.response import Http404
from django.views import View
from django.contrib import messages
from authors.forms import AuthorRecipeForm
from recipes.models import Recipe
from django.shortcuts import redirect, render
from django.urls import reverse


class DashboardRecipe(View): #fazendo por class based views a funcao dashboard_recipe_edit
    def get_recipe(self, id):
        recipe = None

        if id:
            recipe = Recipe.objects.filter(
                is_published = False,
                author = self.request.user,
                pk=id,
            ).first()

            if not recipe:
                raise Http404()
        
        return recipe;
    
    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html', context= {
            'form': form,
        })


    def get(self, request, id):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form)

    
    def Post(self, request, id):
        recipe = self.get_recipe(id);
        
        form = AuthorRecipeForm(
            data = request.POST or None, 
            files=request.FILES or None,
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


    
        return self.render_recipe(form)