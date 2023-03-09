# import json
# from django.http import JsonResponse
from hashlib import sha256
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import Account
from django.contrib.auth import login
from django.contrib import auth
# from django.db.models import Q
# from .forms import  BookForm, userupdateform
from django.views.generic.edit import View
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.views.decorators.cache import cache_control 
# from django.contrib.auth.decorators import login_required
# import razorpay 
from django.conf import settings

def index(request):

    product = Product.objects.all()
    categories = Category.objects.all()
    itms = item.objects.all()
    data = {'product':product, 'categories':categories,'itms':itms}
    return render(request, 'index.html', data)

def showitem(request, iid):
    itms = item.objects.all()
    its = item.objects.get(pk=iid)
    categories = Category.objects.filter(items=its)
    data = {
        # 'itms':itms,
        'categories':categories
    }
    return render(request, 'index.html',data)

def showcategory(request, cid):
    categories = Category.objects.all()
    # obj = Deals.objects.all()
    cats = Category.objects.get(pk=cid)
    product = Product.objects.filter(cat=cats)
    data = {
        # 'categories':categories,
        # 'result': obj,
        'product': product
    }
    return render(request, 'index.html', data)
    
def about(request):
    return render(request,'about.html')

def dashboard(request):
    if 'email' in request.session:
        email=request.session['email']
        return render(request,'dashboard.html',{'name':email})
    return redirect (foodlogin)    
        

def contact(request):
    return render(request,'contact.html')

def services(request):
    return render(request,'services.html')
def packages(request):
    return render(request,'packages.html')

# def login(request):
#     return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword:
            if Account.objects.filter(email=email).exists():
                messages.info(request,"Email Already Exists")
                return redirect('login.html') 
            else:    
                user = Account.objects.create_user(username=username, email=email, phone=phone, password=password)
                user.save()   
                messages.success(request, 'Thank you for registering with us.Please Activate your Email id.') 
                current_site = get_current_site(request)
                message = render_to_string('Account_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
        send_mail(
                'Please activate your account',
                message,
                'parkproject0@gmail.com',
                [email],
                fail_silently=False,
            )
        return redirect(viewlogin) 
    return render(request, 'login.html') 

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('viewlogin')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def viewlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password=request.POST.get('password')
        print(email)
        user = authenticate(email=email ,password=password)
        print(user)
        print(email,password)
        if user :
            print(email,password)
            auth.login(request, user)
            #save email in session
            request.session['email'] = email
            return redirect('index')
        else:
            print(3)
            messages.success(request,"Invalid Credentials")
            return redirect('viewlogin')     
    return render(request,'login.html') 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    auth.logout(request)
    return redirect('viewlogin')   

def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        cpassword = request.POST['confirm_password']
        user = Account.objects.get(email__exact=request.user.email)
        success = user.check_password(current_password)
        if success:
            if new_password==cpassword:
                 user.set_password(new_password)
                 user.save()
                 messages.success(request, 'Password updated successfully.')
                 return redirect('viewlogin')
            else:
                 messages.error(request, 'Password does not match!')
                 return redirect('change_password')
    return render(request, 'change_password.html')     

def foodregistrations(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        pass1=request.POST['password']
        pass2=request.POST['cpassword']
        passwords=sha256(pass2.encode()).hexdigest()
        if food_login.objects.filter(user=email).exists():
            messages.success(request, 'Email already exist....!!!!')
            return redirect('foodregistrations')    
        else:
            log=food_login(user=email,password=passwords)
            log.save()            
            userid=food_login.objects.get(user=email)
            reg=food_registration(username=username,phone=phone,user_id=userid.user,password=passwords)
            # user = Account.objects.create_user(username=username, email=email, phone=phone, password=password)
            reg.save()
            messages.success(request, 'need admin approval')

            return redirect('foodlogin')
    return render(request,'foodlogin.html')

def foodlogin(request):
    request.session.flush()
    if 'email' in request.session:
        return redirect(dashboard)   
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        password2=sha256(password.encode()).hexdigest()
        vol = food_login.objects.filter(user=email,password=password2,type=1)
        if vol:
            vol_details = food_login.objects.get(user=email,password=password2)
            email= vol_details.user
            request.session['email']=email
            return  redirect(dashboard)
        else:
            print("invalid")
            messages.success(request,"invalid login credentials")
            return redirect(foodlogin)
    return render(request,'foodlogin.html')        


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def foodlogout(request):
    if 'email' in request.session:
        request.session.flush()
    return redirect(foodlogin)    


def foodadd(request):
    if request.method == 'POST':
        brandname = request.POST.get('brandname')
        image = request.POST.get('file')
        print(image)
        food_item = fooditem(brandname=brandname, image=image)
        food_item.save()
        messages.success(request, 'Food item added successfully!')
        return redirect('foodadd')
        
    else:
        return render(request, 'foodadd.html')

def fooddis(request):
    if request.method == 'POST':
        data=fooditem.objects.all()
        context={'data': data}
        return render(request,'fooddis.html',context)
    return redirect(dashboard)    
        