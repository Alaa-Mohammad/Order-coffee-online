from django.shortcuts import render,get_object_or_404
from . models import Product 
 
def products(request):
    pro=Product.objects.all()
    ss=None
    if 'searchSensitive' in request.GET:
        ss=request.GET['searchSensitive']
        if not ss:
            ss='off'

    if 'searchName' in request.GET:
        name=request.GET['searchName']
        if name:
            if ss=='on':
                pro=pro.filter(name__contains=name)
            else:
                 pro=pro.filter(name__icontains=name)   

    if 'searchDesc' in request.GET:
        desc=request.GET['searchDesc']
        if desc:
            if ss=='on':
                pro=pro.filter(description__contains=desc)
            else:
                pro=pro.filter(description__icontains=desc)
    if 'searchPriceFrom' in request.GET and 'searchPriceTo' in request.GET:
        pFrom=request.GET['searchPriceFrom']
        pTo=request.GET['searchPriceTo']
        if pFrom and pTo:
            if pFrom.isdigit() and pTo.isdigit():
                pro=pro.filter(price__gte=pFrom,price__lte=pTo)
    context={
        'products':pro
    }
    return render(request,'products/products.html',context)

def product(request,pro_id):
    context={
        "pro":get_object_or_404(Product,pk=pro_id)
    }
    return render(request,'products/product.html',context)

def search(request):
    return render(request,'products/search.html')    