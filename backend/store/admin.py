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

class OrderAddressInline(admin.StackedInline):
    model = OrderAddress
    extra = 1


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
    list_display = ['status', 'created_at', 'updated_at']
    list_filter = ['status']
    inlines = [OrderItemInline, OrderAddressInline, OrderPaymentImageInline]