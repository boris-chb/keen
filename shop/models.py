from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
    
def upload_path(instance, filename):
    return f'{instance.product.category}/{instance.product.name}/{filename}'

class Product(models.Model):
    """
        * Using db_index model attribute to improve query performance.
          (by default, only PK are indexed)
    """
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='upload_path', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name', 'created', 'available',)
        # Index on ID+Slug fields for better query performance on both fields
        index_together = (('id', 'slug'),)
    
    def __str__(self):
        return self.name
    