from django import template
from inventario.models import Producto

register = template.Library()

@register.simple_tag
def get_stock_bajo():
    return Producto.objects.filter(stock__lte=5).count()