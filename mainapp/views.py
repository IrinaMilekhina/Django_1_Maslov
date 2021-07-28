from django.shortcuts import render


def main(request):
    content = {'title': 'Магазин'}
    return render(request, 'mainapp/index.html', content)


def products(request):
    content = {'title': 'Продукты'}
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {'title': 'Контакты'}
    return render(request, 'mainapp/contact.html', content)
