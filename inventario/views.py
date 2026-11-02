from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Producto


@login_required
def inventario_list(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/list.html', {'productos': productos})
