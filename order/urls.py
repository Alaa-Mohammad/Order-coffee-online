from django.urls import path
from . import views

urlpatterns = [
    path('',views.addToCart,name='addToCart'),
    path('cart',views.cart,name='cart'),
    path('<int:orderDetails_id>',views.remove_from_cart,name="remove_from_cart"),
    path('add/<int:orderDetails_id>',views.add_qty,name='add_qty'),
    path('sub/<int:orderDetails_id>',views.sub_qty,name='sub_qty'),
    path('payment',views.payment,name='payment'),
    path('show_orders',views.show_orders,name='show_orders')


]
