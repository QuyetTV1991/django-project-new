from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from myShop.models import Category, Product, Customer, Order

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)

class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'customer'

class UserAdmin(BaseUserAdmin):
    inlines = [CustomerInline]

admin.site.unregister(User)
admin.site.register(Customer)