from django.db import models
from django.contrib.auth.models import User


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sale', 'On sale'),
        ('out', 'Out of stock'),
    ]

    name = models.CharField(max_length=255)

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    product_image = models.ImageField(upload_to='products/', null=True, blank=True)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



class Transaction(models.Model):
    STATUS_CHOICES = [
        ('cart', 'On cart'),
        ('pay', 'To Pay'),
        ('ship', 'To Ship'),
        ('receive', 'To Receive'),
        ('delivered', 'Delivered'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    amount = models.PositiveIntegerField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.amount}"