from django.db import models
from django.contrib.auth.models import User


class CustomManager(models.Manager):
    def get_price_range(self, r1, r2):
        return self.filter(price__range=(r1, r2))

    def Coffee_list(self):
        return self.filter(category__exact="Coffee")

    def Dessert_list(self):
        return self.filter(category__exact="Dessert")

    def Sancks_list(self):
        return self.filter(category__exact="Sancks")


# Create your models here.
class Coffee(models.Model):
    coffee_id = models.IntegerField(primary_key=True)
    coffee_name = models.CharField(max_length=55)
    type = (("Coffee", "Coffee"), ("Dessert", "Dessert"), ("Sancks", "Sancks"))
    category = models.CharField(max_length=100, choices=type, default="")
    desc = models.TextField(max_length=255)
    price = models.IntegerField()
    image = models.ImageField(upload_to="pics")
    objects = models.Manager()
    prod = CustomManager()


class Cart(models.Model):
    coffee_id = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    coffee_id = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)