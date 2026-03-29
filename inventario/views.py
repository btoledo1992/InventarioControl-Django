from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto, Categoria
from .forms import ProductoForm

def dashboard(request):
    total_productos  = Producto.objects.count()
    stock_bajo       = Producto.objects.filter(stock__lte=5).count()
    total_categorias = Categoria.objects.count()
    ultimos          = Producto.objects.order_by('-creado')[:5]
    return render(request, 'dashboard.html', {
        'total_productos':  total_productos,
        'stock_bajo':       stock_bajo,
        'total_categorias': total_categorias,
        'ultimos':          ultimos,
    })

def lista_productos(request):
    q = request.GET.get('q', '')
    productos = Producto.objects.select_related('categoria').all()
    if q:
        productos = productos.filter(nombre__icontains=q)
    return render(request, 'lista.html', {'productos': productos})

def crear_producto(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, '✅ Producto creado correctamente')
        return redirect('lista_productos')
    return render(request, 'formulario.html', {'form': form, 'titulo': '➕ Nuevo Producto'})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if form.is_valid():
        form.save()
        messages.success(request, '✅ Producto actualizado correctamente')
        return redirect('lista_productos')
    return render(request, 'formulario.html', {'form': form, 'titulo': '✏️ Editar Producto'})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, '🗑️ Producto eliminado correctamente')
        return redirect('lista_productos')
    return render(request, 'confirmar_eliminar.html', {'producto': producto})