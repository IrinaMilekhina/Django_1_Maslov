from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from mainapp.models import Product


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super().delete()


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    @cached_property
    def elements(self):
        return Basket.objects.filter(user=self.user).select_related()

    @cached_property
    def product_price(self):
        return self.product.price

    def _get_product_cost(self):
        "return cost of all products this type"
        return self.product.price * self.quantity

    product_cost = property(_get_product_cost)

    def _get_total_quantity(self):
        "return total quantity for user"
        _items = Basket.objects.filter(user=self.user)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    total_quantity = property(_get_total_quantity)

    def _get_total_cost(self):
        "return total cost for user"
        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    total_cost = property(_get_total_cost)

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete()
