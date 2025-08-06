from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('laptops', 'Laptops'),
        ('smartphones', 'Smartphones'),
        ('tvs', 'TVs & Audio'),
        ('gaming', 'Gaming'),
        ('accessories', 'Computer Accessories'),
        ('home', 'Home Appliances'),
        ('networking', 'Networking'),
        ('power', 'Power & Energy'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.name
