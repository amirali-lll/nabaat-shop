from django.db import models
from django.db.models import Model
from django.db import transaction
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


import logging

logger = logging.getLogger(__name__)




class Accessory(Model):
    name         = models.CharField(max_length=255)
    description  = models.TextField(blank=True,null=True)
    cost         = models.DecimalField(max_digits=11,decimal_places=0)
    stock        = models.SmallIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name            = models.CharField(max_length=255)
    parent_category = models.ForeignKey(
        'self',
        related_name='sub_categories',
        on_delete=models.SET_NULL,
        null=True,blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.name


class Plant(Model):
    # products - FK from Product
    
    name         = models.CharField(max_length=255)
    description  = models.TextField(blank=True,null=True)
    cost         = models.DecimalField(max_digits=11,decimal_places=0)
    stock        = models.SmallIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class ProductImage(Model):
    product    = models.ForeignKey('Product',on_delete=models.CASCADE,related_name='images')
    image      = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(Model):
    # rates       - FK from Rate
    # order_items - FK from OrderItem
    # images      - FK from ProductImage
    # reviews     - FK from Review

    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    categories  = models.ManyToManyField(Category,related_name='products',blank=True)
    plants      = models.ManyToManyField(Plant,related_name='products',blank=True)
    accessories = models.ManyToManyField(Accessory,related_name='products',blank=True)
    price       = models.DecimalField(max_digits=11,decimal_places=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    def get_cost(self):
        accessories_cost = self.accessories.aggregate(models.Sum('cost'))['cost__sum'] or 0
        plants_cost = self.plants.aggregate(models.Sum('cost'))['cost__sum'] or 0
        return accessories_cost + plants_cost
    
    def get_stock(self):
        plants_stock      = self.plants.aggregate(models.Min('stock'))['stock__min']
        accessories_stock = self.accessories.aggregate(models.Min('stock'))['stock__min']

        if plants_stock is None and accessories_stock is None:
            return 0
        elif plants_stock is None:
            return accessories_stock
        elif accessories_stock is None:
            return plants_stock
        else:
            return min(plants_stock, accessories_stock)
        
            

class Review(Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    text = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at']


class Rate(Model):
    value = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='rates')
    product = models.ForeignKey('Product',on_delete=models.CASCADE,related_name='rates')


# class Discount(Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='discounts')
#     code = models.CharField(max_length=255)
#     value = models.DecimalField(max_digits=11,decimal_places=0)
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)




class Order(Model):

    STATUS_SUBMITTED = 'S'
    STATUS_PAYMENT_COMPLETED = 'P'
    STATUS_FAILED = 'F'
    STATUS_RETURNED = 'R'
    STATUS_COMPLETED = 'C'
    STATUS_CHOICES = [
        (STATUS_SUBMITTED,_('Submitted')),
        (STATUS_PAYMENT_COMPLETED,_('Payment completed')),
        (STATUS_FAILED,_('Failed')),
        (STATUS_RETURNED,_('Returned')),
        (STATUS_COMPLETED,_('Completed')),
    ]
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=STATUS_SUBMITTED)

    support = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='orders',null=True,blank=True)

    # address        - FK from OrderAddress
    # payment_images - FK from OrderPaymentImage
    # order_items    - FK from OrderItem


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.status + ' - ' + str(self.created_at)


class OrderItem(Model):
    order      = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    product    = models.ForeignKey('Product',on_delete=models.SET_NULL,related_name='order_items',null=True)
    quantity   = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=11,decimal_places=0)
    unit_cost       = models.DecimalField(max_digits=11,decimal_places=0) # calculated from product
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        orig = OrderItem.objects.get(pk=self.pk) if self.pk is not None else None
        if orig is None:
            self.unit_price = self.product.price
            self.unit_cost = self.product.get_cost()
        super().save(*args, **kwargs)
        if orig is None:
            self.update_stock(self.product, -self.quantity)
        elif orig.quantity != self.quantity or orig.product != self.product:
            self.update_stock(orig.product, orig.quantity)
            self.update_stock(self.product, -self.quantity)

    def update_stock(self, product, quantity):
        for accessory in product.accessories.all():
            accessory.stock += quantity
            accessory.save()
        for plant in product.plants.all():
            plant.stock += quantity
            plant.save()
    
    @transaction.atomic
    def delete(self, *args, **kwargs):
        # Increase the stock of the related product before deleting the order item
        self.update_stock(self.product, self.quantity)
        super().delete(*args, **kwargs)
                
                
        
        
    def __str__(self) -> str:
        return self.product.name + ' - ' + str(self.quantity) + ' - ' + str(self.unit_price)


class OrderPaymentImage(Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='payment_images')
    image = models.ImageField(upload_to='orders/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderAddress(Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name='address')
    city = models.CharField(max_length=255)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    location = models.URLField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.city + ' - ' + self.postal_code