from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    reorder_level = models.IntegerField(default=5)

    def __str__(self):
        return self.name