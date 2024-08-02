import datetime
from django.db import models
from django import forms


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='upload/product')
    description= models.CharField(max_length=25000, default='None', blank=True, null=True)
    
    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids)
    
    @staticmethod
    def get_all_products():
        return Products.objects.all()
    
    @staticmethod
    
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_products()
        
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    
    def register(self):
        self.save()
        
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
        
    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True
        
        return False
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
    
    
class Order(models.Model):
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField (max_length=50, default='Hanoi', blank=True)
    phone = models.CharField (max_length=50, default='0123456789', blank=True)
    date = models.DateField (default=datetime.datetime.today)
    status = models.BooleanField (default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

    def __str__(self):
        return str(self.product) + "    SL: " + str(self.quantity)


class Order_Item(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return id
    
    def price_per_unit(self):
        return self.quantity * self.product.price

    # order = models.ForeignKey('Order', on_delete=models.CASCADE)
    # product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    # quantity = models.PositiveIntegerField()
    # unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    # total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
# class ProductSearchForm(forms.Form):
#     # Lấy data từ user khi nhập vào form tìm kiếm
#     search_query = forms.CharField(max_length=100)