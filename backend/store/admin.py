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
    list_display = ['status', 'created_at', 'updated_at']
    list_filter = ['status']
    inlines = [OrderItemInline, OrderPaymentImageInline]
    autocomplete_fields = ['address', 'customer']
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    inlines = [AddressInline]
    search_fields = ['user__username','user__email','user__first_name','user__last_name']
    
    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'city', 'address', 'postal_code', 'created_at', 'updated_at']
    search_fields = ['city', 'address', 'postal_code']
    list_filter = ['city']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "customer":
            kwargs["queryset"] = Customer.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    