from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product

def index(request):
    context={
        'products':Product.objects.all()
    }
    return render(request,'test1/index.html',context)

def about(request):
    return render(request,'test1/about.html') 

def coffee(request):
    return render(request,'test1/coffee.html')
    
