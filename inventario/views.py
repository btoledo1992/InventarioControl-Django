from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Producto, Categoria
from .forms import ProductoForm
from django.http import HttpResponse
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

# ── LOGIN ──────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

# ── LOGOUT ─────────────────────────────────────────
def logout_view(request):
    logout(request)
    return redirect('login')

# ── DASHBOARD ──────────────────────────────────────
@login_required(login_url='login')
def dashboard(request):
    import json
    total_productos  = Producto.objects.count()
    stock_bajo       = Producto.objects.filter(stock__lte=5).count()
    total_categorias = Categoria.objects.count()
    ultimos          = Producto.objects.order_by('-creado')[:5]

    # Datos para gráfico de stock por categoría
    categorias       = Categoria.objects.all()
    labels_cat       = [c.nombre for c in categorias]
    data_cat         = [Producto.objects.filter(categoria=c).aggregate(
                            total=models.Sum('stock'))['total'] or 0
                        for c in categorias]

    # Datos para gráfico de productos por talle
    talles           = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
    data_talles      = [Producto.objects.filter(talle=t).count() for t in talles]

    return render(request, 'dashboard.html', {
        'total_productos':  total_productos,
        'stock_bajo':       stock_bajo,
        'total_categorias': total_categorias,
        'ultimos':          ultimos,
        'labels_cat':       json.dumps(labels_cat),
        'data_cat':         json.dumps(data_cat),
        'labels_talles':    json.dumps(talles),
        'data_talles':      json.dumps(data_talles),
    })

# ── PRODUCTOS ──────────────────────────────────────
@login_required(login_url='login')
def lista_productos(request):
    q = request.GET.get('q', '')
    productos = Producto.objects.select_related('categoria').all()
    if q:
        productos = productos.filter(nombre__icontains=q)
    return render(request, 'lista.html', {'productos': productos})

@login_required(login_url='login')
def crear_producto(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, '✅ Producto creado correctamente')
        return redirect('lista_productos')
    return render(request, 'formulario.html', {'form': form, 'titulo': '➕ Nuevo Producto'})

@login_required(login_url='login')
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if form.is_valid():
        form.save()
        messages.success(request, '✅ Producto actualizado correctamente')
        return redirect('lista_productos')
    return render(request, 'formulario.html', {'form': form, 'titulo': '✏️ Editar Producto'})

@login_required(login_url='login')
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, '🗑️ Producto eliminado correctamente')
        return redirect('lista_productos')
    return render(request, 'confirmar_eliminar.html', {'producto': producto})

@login_required(login_url='login')
def exportar_excel(request):
    # Crear el archivo Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Productos"

    # Estilo del encabezado
    header_font  = Font(bold=True, color="FFFFFF")
    header_fill  = PatternFill(start_color="570df8", end_color="570df8", fill_type="solid")
    header_align = Alignment(horizontal="center")

    # Encabezados
    columnas = ['ID', 'Nombre', 'Categoría', 'Talle', 'Color', 'Precio', 'Stock', 'Fecha']
    for col_num, columna in enumerate(columnas, 1):
        cell = ws.cell(row=1, column=col_num, value=columna)
        cell.font  = header_font
        cell.fill  = header_fill
        cell.alignment = header_align

    # Ancho de columnas
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 15
    ws.column_dimensions['G'].width = 10
    ws.column_dimensions['H'].width = 20

    # Datos
    productos = Producto.objects.select_related('categoria').all()
    for row_num, producto in enumerate(productos, 2):
        ws.cell(row=row_num, column=1, value=producto.id)
        ws.cell(row=row_num, column=2, value=producto.nombre)
        ws.cell(row=row_num, column=3, value=producto.categoria.nombre if producto.categoria else '')
        ws.cell(row=row_num, column=4, value=producto.talle)
        ws.cell(row=row_num, column=5, value=producto.color)
        ws.cell(row=row_num, column=6, value=float(producto.precio))
        ws.cell(row=row_num, column=7, value=producto.stock)
        ws.cell(row=row_num, column=8, value=producto.creado.strftime('%d/%m/%Y %H:%M'))

    # Devolver el archivo
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="productos.xlsx"'
    wb.save(response)
    return response