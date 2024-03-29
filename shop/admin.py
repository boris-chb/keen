from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'slug']
    prepopulated_fields = {'slug': ('gender', 'name')}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'size', 'quantity', 'available']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available', 'quantity', 'size']
    prepopulated_fields = {'slug': ('name',)} # Auto-generated
