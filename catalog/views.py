from django.shortcuts import render
from catalog.models import Category

# Create your views here.
def index(request):
    category_list = Category.objects.all()
    context = {
        'object_list': category_list
    }
    return render(request, 'catalog/main.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        name = request.POST.get('phone')
        name = request.POST.get('message')
        print(f'{name} ({phone})')
    return render(request, 'catalog/contacts.html')
