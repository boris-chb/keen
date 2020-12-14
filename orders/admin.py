from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.core import serializers

################################################
## [+] Exports Order information to .CSV file ##
################################################

def export_to_csv(modeladmin, request, queryset):
    options = modeladmin.model._meta
    # Specify there's an attached file in the response
    content_disposition = f'attachment; filename={options.verbose_name}.csv'
    # Make browser treat response as .CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    # CSV-Writer to write to response object
    writer = csv.writer(response)
    
    # Exclude Many-To-Many and One-To-Many relationships
    fields = [field for field in options.get_fields() if not field.many_to_many and not field.one_to_many]
    # First row with header info
    writer.writerow([field.verbose_name for field in fields])
    # Data rows
    for element in queryset:
        data_row = []
        for field in fields:
            value = getattr(element, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'country', 'paid']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


