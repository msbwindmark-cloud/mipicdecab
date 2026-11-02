from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count


@login_required
def ranking_list(request):
    usuarios = User.objects.annotate(num_logros=Count('logros')).order_by('-num_logros', 'username')
    context = {
        'usuarios': usuarios,
        'top3': usuarios[:3],
    }
    return render(request, 'ranking/list.html', context)
