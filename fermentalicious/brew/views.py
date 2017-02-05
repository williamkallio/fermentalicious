from django.shortcuts import render

from .models import Beverage

def index(request):
    beverage_list = Beverage.objects.order_by('-create_datetime')
    context = {'beverage_list' : beverage_list}
    return render(request, 'brew/index.html', context)

def detail(request, beverage_id):
    try:
        beverage = Beverage.objects.get(pk=beverage_id)
    except Beverage.DoesNotExist:
        raise Http404("Beverage does not exist...man")
    return render(request, 'brew/detail.html', {'beverage' : beverage})
