from django.shortcuts import render ,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from accounts.models import UserProfile 
import re
def signup(request):
    if request.method=='POST' and "btnsignup" in request.POST:
        #variables for fields
        fname,lname,address1,address2,city,state,zip_number,email,username,password,terms,is_add=[None for i in range(12)]

        #get values from the form
        if "fname" in request.POST:
            fname=request.POST['fname']
        else:
            messages.error(request,"error in first name")
        if "lname" in request.POST:
            lname=request.POST['lname']
        else:
            messages.error(request,"error in last name")
        if "address1" in request.POST:
            address1=request.POST['address1']
        else:
            messages.error(request,"error in address1")
        if "address2" in request.POST:
            address2=request.POST['address2']
        else:
            messages.error(request,"error in address2")
        if "city" in request.POST:
            city=request.POST['city']
        else:
            messages.error(request,"error in city name")  
        if "state" in request.POST:
            state=request.POST['state']
        else:
            messages.error(request,"error in state name")
        if "zip_number" in request.POST:
            zip_number=request.POST['zip_number']
        else:
            messages.error(request,"error in zip number") 
        if "username" in request.POST:
            username=request.POST['username']
        else:
            messages.error(request,"error in user name")    
        if "email" in request.POST:
            email=request.POST['email']
        else:
            messages.error(request,"error in email")
        if "password" in request.POST:
            password=request.POST['password']
        else:
            messages.error(request,"error in password")   
        
        #check the values
        if fname and lname and address1 and address2 and city and state and zip_number and email and username and password:
            if "terms" in request.POST:
                terms=request.POST['terms']

                if User.objects.filter(username=username).exists():
                    messages.error(request,"This username already exists")
                else:    
                    if User.objects.filter(email=email).exists():
                        messages.error(request,"This email already exists")
                    else:
                        pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                        if re.fullmatch(pattern,email):
                            user=User.objects.create_user(first_name=fname,
                                                        last_name=lname,email=email,username=username,
                                                        password=password)
                            user.save()               
                            #add user profile
                            userprofile=UserProfile(user=user,address1=address1,address2=address2,
                                                    city=city,state=state,zip_number=zip_number)   
                            userprofile.save()

                            #clear fields
                            fname,lname,address1,address2,city,state,zip_number,email,username,password,terms=['' for i in range(11)]

                            #success message
                            messages.success(request,"your account is created")
                            is_add=True 

                        else:
                            messages.error(request,"invalid email")
            else:
                messages.error(request,"you don't agree to the terms")
        else:
            messages.error(request,"check empty fields")    

        context={'fname':fname,'lname':lname,'address1':address1,'address2':address2,\
                 'city':city,'state':state,'zip_number':zip_number,'username':username,\
                  'password':password,'email':email,'is_add':is_add}
        return render(request,'accounts/signup.html',context)
         
    else:    
        return render(request,'accounts/signup.html')

def signin(request):
    if request.method=='POST' and 'btnsignin' in request.POST:
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request,user)
            messages.success(request,"You are logged in now")
        else:
            messages.error(request,"username or password invalid")    
    return render(request,'accounts/signin.html')    

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return render(request,'test1/index.html') 

def profile(request):
    if request.method=="POST" and "btnsave" in request.POST:
        if request.user is not None and request.user.id != None:
            userprofile=UserProfile.objects.get(user=request.user)
            if request.POST['fname'] and request.POST['lname'] and request.POST['address1'] and request.POST['address2']\
                and request.POST['city'] and request.POST['state'] and request.POST['zip_number'] and request.POST['email']\
                and request.POST['username'] and request.POST['password']:
                request.user.first_name=request.POST['fname']
                request.user.last_name=request.POST['lname']
                userprofile.address1=request.POST['address1']
                userprofile.address2=request.POST['address2']
                userprofile.city=request.POST['city']
                userprofile.state=request.POST['state']
                userprofile.zip_number=request.POST['zip_number']
                if not request.POST['password'].startswith("pbkdf2_sha256$260000$"):
                    request.user.set_password(request.POST['password'])

                request.user.save()
                userprofile.save()    
                auth.login(request,request.user)
                messages.success(request,"Your data has been saved")

            else:
                messages.error(request,"check your input values")

        return redirect('profile')    
    else:
        context=None
        if request.user.username is not None:
            if not request.user.is_anonymous:
                userprofile=UserProfile.objects.get(user=request.user)
                context={
                    'fname':request.user.first_name,
                    'lname':request.user.last_name,
                    'username':request.user.username,
                    'password':request.user.password,
                    'email':request.user.email,
                    'address1':userprofile.address1,
                    'address2':userprofile.address2,
                    'city':userprofile.city,
                    'state':userprofile.state,
                    'zip_number':userprofile.zip_number
                       }
            return render(request,'accounts/profile.html',context)         


from accounts.models import Product
def product_favorite(request,pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous: 
        pro_fav=Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user,product_favorites=pro_fav).exists():
            messages.error(request,"The product is already in the favorite list")
        else:
            userprof=UserProfile.objects.get(user=request.user)
            userprof.product_favorites.add(pro_fav)
            messages.success(request,"The product has been added to your favourite list")
        return redirect('/products/'+ str(pro_id)) 
    else:
        return redirect('profile')        


def show_product_favorite(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous: 
        userInfo=UserProfile.objects.get(user=request.user)
        pro=userInfo.product_favorites.all()
        context={'products':pro}
    return render(request,'products/products.html',context)    

