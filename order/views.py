from django.shortcuts import render,redirect
from products.models import Product
from order.models import Order,OrderDetails,Checkout
from django.utils import timezone
from django.contrib import messages

def addToCart(request):
    if request.user.is_authenticated and not request.user.is_anonymous: 
        if request.method=="POST" and 'pro_id' in request.POST and 'qty' in request.POST:
            pro_id=request.POST['pro_id']
            qty=request.POST['qty']
            order=Order.objects.filter(user=request.user,is_finished=False)           
            pro=Product.objects.get(id=pro_id)

            if not Product.objects.filter(id=pro_id).exists():
                return redirect('/products/products')

            if order:
                old_order=Order.objects.get(user=request.user,is_finished=False)
                if OrderDetails.objects.filter(order=old_order,product=pro).exists():
                    order_details=OrderDetails.objects.get(order=old_order,product=pro)
                    order_details.quantity += int(qty)
                    order_details.save()
                else:   
                    OrderDetails.objects.create(order=old_order,product=pro,price=pro.price,quantity=qty)

                messages.success(request,"it has added this product to your cart")

            else:
                new_order=Order()
                new_order.user=request.user
                new_order.order_date=timezone.now()
                new_order.is_finished=False
                new_order.save()
                 
                OrderDetails.objects.create(order=new_order,product=pro,price=pro.price,quantity=qty)
                messages.success(request,"it has added this product to your cart")

            return redirect('/products/'+request.POST['pro_id'])
    else:
        messages.error(request,"please sign in before add any product")
        return redirect('/products/products/'+request.POST['pro_id'])


def cart(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous: 
        if Order.objects.filter(user=request.user,is_finished=False):
            order=Order.objects.get(user=request.user,is_finished=False)
            order_details=OrderDetails.objects.filter(order=order)
            total=0
            for sub in order_details:
                total += sub.price * sub.quantity
            context={
                'order':order,
                'orderDetails':order_details,
                'total':total
            }    

    return render(request,'orders/cart.html',context)

def remove_from_cart(request,orderDetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous: 
        if orderDetails_id:
            orderDetails=OrderDetails.objects.get(id=orderDetails_id)
            if orderDetails.order.user.id ==request.user.id:
                orderDetails.delete()
    return redirect('cart')        


def add_qty(request,orderDetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous: 
        if orderDetails_id:
            order_Details=OrderDetails.objects.get(id=orderDetails_id)
            if order_Details.order.user.id ==request.user.id:
                order_Details.quantity +=1
                order_Details.save()

    return redirect('cart')

def sub_qty(request,orderDetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous: 
        if orderDetails_id :
            order_Details=OrderDetails.objects.get(id=orderDetails_id)
            if order_Details.order.user.id ==request.user.id:
                if order_Details.quantity >1:
                    order_Details.quantity -=1
                    order_Details.save()

    return redirect('cart')    


def payment(request):
    context,ship_address,ship_phone,card_number,expire,security_code=[None for i in range(6)]
    if request.method=='POST' and 'btnpayment' in request.POST and 'ship_address' in request.POST and\
       'ship_phone' in request.POST and 'card_number' in request.POST and 'expire' in request.POST and\
        'security_code' in request.POST:
        ship_address=request.POST['ship_address']
        ship_phone=request.POST['ship_phone']
        card_number=request.POST['card_number']
        expire=request.POST['expire']
        security_code=request.POST['security_code']
        if request.user.is_authenticated and not request.user.is_anonymous: 
             if Order.objects.filter(user=request.user,is_finished=False):
                order=Order.objects.get(user=request.user,is_finished=False)
                checkout=Checkout(order=order,shipment_address=ship_address,shipment_phone=ship_phone,card_number=card_number,
                                  expire=expire,security_code=security_code)
                checkout.save()       
                order.is_finished=True
                order.save()    
                messages.success(request,'your order is finished')       


    else:
        if request.user.is_authenticated and not request.user.is_anonymous: 
            if Order.objects.filter(user=request.user,is_finished=False):
                order=Order.objects.get(user=request.user,is_finished=False)
                order_details=OrderDetails.objects.filter(order=order)
                total=0
                for sub in order_details:
                    total += sub.price * sub.quantity
                context={
                    'order':order,
                    'orderDetails':order_details,
                    'total':total
                }    

    return render(request,'orders/payment.html',context) 


def show_orders(request):
    context,all_orders=[None for i in range(2)]
    if request.user.is_authenticated and not request.user.is_anonymous: 
            all_orders=Order.objects.filter(user=request.user)
            if all_orders:
                for x in all_orders:
                    order=Order.objects.get(id=x.id)
                    order_details=OrderDetails.objects.filter(order=order)
                    total=0
                    for sub in order_details:
                        total += sub.price * sub.quantity

                    x.total= total
                    x.items_count=order_details.count
                    x.save()
                context={
                    'allOrders':all_orders,
                        }   

    return render(request,'orders/show_orders.html',context)       