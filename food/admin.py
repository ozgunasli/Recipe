from django.contrib import admin
from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Ingredient)

class IngredientAdmin(admin.ModelAdmin):
    fields = ('ingredient',)
    list_display = ('ingredient',)
    list_filter = ('ingredient',)
    search_fields = ('ingredient',)
    class Meta:
        model=Ingredient

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('name','user','ingredients','description','difficulty','image',)
    list_display = ('name','publishing_date',)
    list_filter = ('name',)
    search_fields = ('name',)


