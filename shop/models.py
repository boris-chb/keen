from django.db import models
from django.urls import reverse
import os

def upload_path(instance, filename):
    filename = f'{instance.name}.png'
    return f'products/{instance.category}/{instance.slug}/{filename}'

class Category(models.Model):
    GENDER_CHOICES = (
        ('men', 'Men'),
        ('women', 'Women'),
    )
    
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default='Men')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])
        
    def __str__(self):
        return f'{self.gender} {self.name}'



class Product(models.Model):
    """
        * Using db_index model attribute to improve query performance.
          (by default, only PK are indexed)
    """

    SIZE_CHOICES = (
        ('2', 'UK2'),
        ('2.5', 'UK2.5'),
        ('3', 'UK3'),
        ('3.5', 'UK3.5'),
        ('4', 'UK4'),
        ('4.5', 'UK4.5'),
        ('5', 'UK5'),
        ('5.5', 'UK5.5'),
        ('6', 'UK6'),
        ('6.5', 'UK6.5'),
        ('7', 'UK7'),
        ('7.5', 'UK7.5'),
        ('8', 'UK8'),
        ('8.5', 'UK8.5'),
        ('9', 'UK9'),
        ('9.5', 'UK9.5'),
        ('10', 'UK10')
        )
    
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to=upload_path, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, default='8')
    quantity = models.IntegerField(default=1)
    
    class Meta:
        ordering = ('name', 'created', 'available',)
        # Index on ID+Slug fields for better query performance on both fields
        index_together = (('id', 'slug'),)
    
    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
    
    def __str__(self):
        return self.name

