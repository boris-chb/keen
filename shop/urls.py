from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'shop'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('products/', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
