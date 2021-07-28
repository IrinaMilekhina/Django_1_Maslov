import json
import os

from django.shortcuts import render

from mainapp.models import Product, ProductCategory

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


def main(request):
    title = 'главная'
    products = Product.objects.all()[:4]

    content = {
        'title': title,
        'products': products,
        # 'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    same_products = Product.objects.all()[:4]
    links_menu = ProductCategory.objects.all()
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'same_products': same_products
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    locations = load_from_json('contact__locations')
    content = {
        'title': 'Контакты',
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', content)
