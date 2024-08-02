from django.contrib import admin
from django.urls import path
from .views import Index 
from .views import Signup
from .views import Login , logout
from .views import Cart
from .views import CheckOut
from .views import OrderView
from .middlewares.auth import  auth_middleware
from .views import Change
from .views import store
from .views import detail_product

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),

    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    # path('delete_product/<int:product_id>/', Change.delete_product, name='delete_product'),
    # path('add_to_cart', Change.delete_product, name='delete_product'),
    path('up_cart', Change.up_cart, name='up_cart'),
    path('down_cart', Change.down_cart, name='down_cart'),
    path('detail/<int:product_id>', detail_product, name='detail_product'),
    # path('delete_item/<int:product_id>/', Delete.as_view(), name='delete_product'),
    # path('checkout/delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
]


