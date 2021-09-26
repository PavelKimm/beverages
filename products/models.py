from django.db import models


class Product(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    # class Meta:
    #     abstract = True
