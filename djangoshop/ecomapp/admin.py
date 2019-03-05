from django.contrib import admin
from ecomapp.models import *
# Register your models here.



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price','available']
    list_editable = ['price','available']
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category,CategoryAdmin)#Здесь прописал код из другого источника
admin.site.register(Product,ProductAdmin)#Здесь прописал код из другого источника
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
