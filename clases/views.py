from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Clase, Instructor


@login_required
def clase_list(request):
    clases = Clase.objects.select_related('instructor', 'pista').all().order_by('-fecha')
    return render(request, 'clases/list.html', {'clases': clases})


@login_required
def clase_create(request):
    return redirect('clase_list')
