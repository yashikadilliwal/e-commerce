from django.db import models
from autoslug import AutoSlugField

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=AutoSlugField(populate_from='name', unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=100)
    slug=AutoSlugField(populate_from='name', unique=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
