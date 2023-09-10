from django.contrib import admin
from .models import Category, Recipe

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    ...

admin.site.register(Category, CategoryAdmin)

#Registrando outra maneira abaixo:
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published']
    list_display_links = ['title','created_at']
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps'
    list_filter = 'category', 'author', 'is_published', 'preparation_steps_is_html'
    list_per_page = 10
    list_editable = ['is_published']
    prepopulated_fields = {
        "slug": ('title',) #colocar slug baseado no titulo automaticamente ao criar receitas
    }

