from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    reorder_level = models.IntegerField(default=5)

    def __str__(self):
        return self.name

        

class Sale(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sales"
    )

    quantity = models.PositiveIntegerField()

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    sold_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Calculate the total amount
        self.total_amount = self.quantity * self.selling_price

        # Only reduce stock when creating a new sale
        if not self.pk:

            # Check if enough stock exists
            if self.quantity > self.product.quantity:
                raise ValidationError(
                    f"Only {self.product.quantity} item(s) of {self.product.name} are available in stock."
                )

            # Reduce the stock
            self.product.quantity -= self.quantity
            self.product.save()

        # Save the sale
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Mpesa', 'Mpesa'),
        ('Card', 'Card'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_code = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    paid_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"{self.payment_method} - KSh {self.amount}"