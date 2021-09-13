from django.core.management import BaseCommand
from django.db.models import Q, F, When, Case, IntegerField

from mainapp.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Использование ИЛИ
        query_1 = Q(category_name='дом')
        query_2 = Q(category_name='офис')
        products_list = Product.objects.filter(query_1 | query_2)
        print(products_list)

        # Решение задачи посложнее
        sale_under_3000 = 0.1
        sale_3000_5000 = 0.2
        sale_above_5000 = 0.3

        product_under_3000 = Q(price__lte=3000)
        product_3000_5000 = Q(price__gte=3000, price__lte=5000)
        product_above_5000 = Q(price__gte=5000)

        product_under_3000_when = When(product_under_3000, then=3)
        product_3000_5000_when = When(product_3000_5000, then=5)
        product_above_5000_when = When(product_above_5000, then=7)

        product_sale_price_under_3000 = When(product_under_3000, then=F('price') * sale_under_3000)
        product_sale_price_3000_5000 = When(product_3000_5000, then=F('price') * sale_3000_5000)
        product_sale_price_above_5000 = When(product_above_5000, then=F('price') * sale_above_5000)

        sale_products = Product.objects.annotate(
            choise_sale=Case(
                product_under_3000_when,
                product_3000_5000_when,
                product_above_5000_when,
                output_field=IntegerField(),
            )
        ).annotate(
            sale_price=Case(
                product_sale_price_under_3000,
                product_sale_price_3000_5000,
                product_sale_price_above_5000,
                output_field=IntegerField(),
            )
        ).order_by('sale_price')

        for orderitem in sale_products:
            print(f'{orderitem.name} - {orderitem.choise_sale} - {orderitem.sale_price}')