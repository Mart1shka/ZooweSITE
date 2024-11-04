from django.db import models
from django.contrib.auth.models import User
import uuid

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    quantity = models.IntegerField(default=0)
    image1 = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/', blank=True, null=True)
    image5 = models.ImageField(upload_to='products/', blank=True, null=True)
    image6 = models.ImageField(upload_to='products/', blank=True, null=True)
    image7 = models.ImageField(upload_to='products/', blank=True, null=True)
    image8 = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} in cart of {self.user.username}'

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)  # Предположим, пользователь с id=1 существует
    items = models.ManyToManyField(CartItem)

    def __str__(self):
        return f'Cart of {self.user.username}'

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('novaposhta', 'Новая почта'),
        ('ukrposhta', 'Укр почта'),
        ('meest', 'Meest'),
        ('instore', 'В магазин'),
    ]
    DELIVERY_TYPE_CHOICES = [
        ('courier', 'Курьером'),
        ('branch', 'В отделение'),
        ('postamat', 'В почтомат'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller', null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Оплачен', choices=[('оплачен', 'Оплачен'), ('доставляется', 'Доставляется'), ('доставлен', 'Доставлен')])
    first_name = models.CharField(max_length=50, default='Unknown')
    last_name = models.CharField(max_length=50, default='Unknown')
    email = models.EmailField(default='example@example.com')
    delivery_service = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='novaposhta')
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES, null=True, blank=True)
    branch_number = models.IntegerField(null=True, blank=True, default=0)
    postal_index = models.CharField(max_length=10, null=True, blank=True)
    store_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)  # Исправлено на max_length
    postamat_number = models.CharField(max_length=10, null=True, blank=True)
    order_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f'Order {self.order_number} for {self.user.username}'




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

