from django.contrib import admin
from home.models import Category, Product

class ProductAdmin(admin.ModelAdmin):
    exclude = ['slug']
    raw_id_fields = ('category',)

class CategoryAdmin(admin.ModelAdmin):
    exclude = ['slug']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
