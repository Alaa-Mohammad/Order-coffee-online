from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from products.models import Product
from creditcards.models import CardNumberField,CardExpiryField,SecurityCodeField

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_date=models.DateTimeField()
    details=models.ManyToManyField(Product,through='orderDetails')
    is_finished=models.BooleanField()
    total=0
    items_count=0

    def __str__(self):
        return 'User: ' + self.user.username +'order id: '+ str(self.id)     


class OrderDetails(models.Model):
    product=models.ForeignKey(Product,on_delete=CASCADE)
    order=models.ForeignKey(Order,on_delete=CASCADE)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    quantity=models.IntegerField()

    def __str__(self):
        return 'User: ' + self.order.user.username +' , Product: '+ self.product.name + 'Order id: ' + str(self.order.id)

    class Meta:
        ordering=['-id']    


class Checkout(models.Model):
    order=models.ForeignKey(Order,on_delete=CASCADE)
    shipment_address=models.CharField(max_length=50)
    shipment_phone=models.CharField(max_length=50)
    card_number=CardNumberField()
    expire=CardExpiryField()
    security_code=SecurityCodeField()    