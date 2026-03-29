from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'talle', 'color', 'precio', 'stock']
    list_filter  = ['categoria', 'talle']
    search_fields = ['nombre', 'color']