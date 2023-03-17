# import json
# from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from hashlib import sha256
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render,redirect,get_object_or_404
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
import razorpay 
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
        image = request.FILES.get('image')
        print(image)
        food_item = fooditem(brandname=brandname, image=image)
        food_item.save()
        messages.success(request, 'Food item added successfully!')
        return redirect('foodadd')
    else:
        return render(request, 'foodadd.html')


def fooddis(request):
    if 'email' in request.session:
        data=fooditem.objects.all()
        context={'data': data}
        return render(request,'fooddis.html',context)
    return redirect(dashboard)    
        
def Delete(request,id):
    food=fooditem.objects.filter(id=id)
    food.delete()
    messages.info(request,"Deleted")
    return redirect(fooddis)        


def edit_food_item(request, pk):
    item = get_object_or_404(fooditem, pk=pk)

    if request.method == 'POST':
        # If the request method is POST, update the fooditem object with the new data
        item.brandname = request.POST['brandname']
        item.image = request.FILES['image']
        item.save()

        # Redirect to the fooditem detail page after editing the fooditem object
        return redirect('fooddis')
    else:
        # If the request method is GET, render the edit fooditem form with the current data
        return render(request, 'edit_food_item.html', {'item': item}) 



def add_food_category(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_image = request.FILES.get('category_image')
        item_id = request.POST.get('item_id')
        if title and category_image and item_id:
            item_instance = get_object_or_404(fooditem, pk=item_id)
            category = foodCategory.objects.create(title=title, category_image=category_image, items=item_instance)
            return redirect('food_category_dis')
        else:
            return HttpResponseBadRequest('Title, category image, and item ID are required')
    items = fooditem.objects.all()
    return render(request, 'add_food_category.html', {'items': items})   


def edit_food_category(request, pk):
    category = get_object_or_404(foodCategory, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        category_image = request.FILES.get('category_image')
        item_id = request.POST.get('item_id')
        if title and category_image and item_id:
            item_instance = get_object_or_404(item, pk=item_id)
            category.title = title
            category.category_image = category_image
            category.items = item_instance
            category.save()
            return redirect('food_category_dis')
        else:
            return HttpResponseBadRequest('Title, category image, and item ID are required')
    items = item.objects.all()
    return render(request, 'edit_food_category.html', {'category': category, 'items': items})  

def food_category_dis(request):
    if 'email' in request.session:
        data=foodCategory.objects.all()
        context={'data': data}
        return render(request,'food_category_dis.html',context)
    return redirect(dashboard)

# def delete_food_category(request, pk):
#     # category = get_object_or_404(foodCategory, pk=pk)
#     category=foodCategory.objects.filter(pk=pk)
#     if request.method == 'POST':
#         category.delete()
#         return redirect(food_category_dis)
#     return render(request, 'food_category_dis.html')    


 
def delete_food_category(request,id):
    category=foodCategory.objects.filter(id=id)
    category.delete()
    messages.info(request,"Deleted")
    return redirect(food_category_dis)  



#booking

import razorpay

@login_required
def booking(request):
    if request.method == 'POST':
        user = request.user
        p1_id = request.POST.get('p1_id')
        p2_id = request.POST.get('p2_id')
        date = request.POST.get('date')
        count_adult = int(request.POST.get('count1', 1))
        count_child = int(request.POST.get('count2', 0))

        try:
            p1 = Adultpackage.objects.get(p1_id=p1_id)
        except Adultpackage.DoesNotExist:
            p1 = None
        try:
            p2 = Childpackage.objects.get(p2_id=p2_id)
        except Childpackage.DoesNotExist:
            p2 = None

        if p1 is None:
            messages.error(request, 'Invalid package selected.')
            return redirect('booking')

        total_price = (count_adult * p1.price) + (count_child * p2.price)
        booking = Book.objects.create(user=user, p1_id=p1, p2_id=p2, date=date, count_adult=count_adult, count_child=count_child, total_price=total_price)
        messages.success(request, 'Booking successful.')
        return redirect('checkout', booking.id)
    
    # Get all available packages for the form
    adult_packages = Adultpackage.objects.all()
    child_packages = Childpackage.objects.all()

    return render(request, 'booking.html', {'adult_packages': adult_packages, 'child_packages': child_packages})
    
def checkout(request, booking_id):
    
 
        latest_booking = Book.objects.get(id=booking_id)
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
        data = {
            'amount': latest_booking.total_price * 100,  # Convert to paise
            'currency': 'INR',
            'receipt': str(latest_booking.id),
            'payment_capture': 1,
        }
        order = client.order.create(data=data)
        order_id = order['id']
        request.session['order_id'] = order_id
        request.session['booking_id'] = booking_id
        
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        order_status = order['status']
        if order_status == 'created':
            payment = Payments.objects.create(
                user=latest_booking.user,
                amount=latest_booking.total_price,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status,
                razorpay_payment_id = razorpay_payment_id,
                paid=False
            )
            latest_booking.payment = payment
            latest_booking.save()
            # return redirect(request,'success.html')

        return render(request, 'checkout.html', {'latest_booking': latest_booking, 'order_id': order_id})



def paymentdone(request):
    order_id=request.GET.get('razorpay_order_id')
    payment_id=request.POST.get('razorpay_payment_id')
    print(order_id)
    print(payment_id)
    user=request.user   
    try:
        payment=Payments.objects.get(razorpay_order_id=order_id)
    except Payments.DoesNotExist:
        return HttpResponse("Payment does not exist for the given order ID") 
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()   
    booking=Book.objects.get(id=request.session['booking_id'])
    Placed_Booking.objects.create(
        user=user,
        p1_id=booking.p1_id,
        p2_id=booking.p2_id,
        date=booking.date,
        payment=payment
    )
    booking.delete()
    return redirect('index')
