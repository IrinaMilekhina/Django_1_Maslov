from django.shortcuts import render


def main(request):
    content = {}
    return render(request, 'mainapp/index.html', content)


def products(request):
    return render(request, 'mainapp/products.html')


def contact(request):
    return render(request, 'mainapp/contact.html')
