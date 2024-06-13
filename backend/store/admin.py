from django.contrib import admin
from .models import *

@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'stock', 'created_at', 'updated_at']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['parent_category']

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'stock', 'created_at', 'updated_at']
    search_fields = ['name']
    
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'created_at', 'updated_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']



class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0

class RateInline(admin.StackedInline):
    model = Rate
    extra = 0

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['unit_cost', 'unit_price']

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0
    
class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = 'User'

class OrderPaymentImageInline(admin.StackedInline):
    model = OrderPaymentImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'cost', 'stock' ,'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['categories' ,'plants', 'accessories']
    readonly_fields = ['cost', 'stock']
    inlines = [ProductImageInline, ReviewInline, RateInline]
    
    def cost(self, obj):
        return obj.get_cost()
    
    def stock(self, obj):
        return obj.get_stock()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_price', 'status', 'created_at', 'updated_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'customer__email', 'customer__phone_number']
    list_filter = ['status']
    inlines = [OrderItemInline, OrderPaymentImageInline, AddressInline]
    autocomplete_fields = ['customer']
    readonly_fields = ['total_price', 'total_cost']
    
    def total_price(self, obj):
        return obj.get_total_price()
    
    def total_cost(self, obj):
        return obj.get_total_cost()
    
    
    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['city', 'address', 'postal_code', 'created_at', 'updated_at']
    search_fields = ['city', 'address', 'postal_code']
    list_filter = ['city']