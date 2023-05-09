# import json
# from django.http import JsonResponse
import base64
import os
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from hashlib import sha256
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
import pandas as pd
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
    # food1=fooditem.objects.all()
    food2=foodCategory.objects.all()
    food3=Product.objects.all()
    reviews=review.objects.all()
    data = {'product':product, 'categories':categories,'itms':itms ,'food2':food2,'food3':food3,'reviews':reviews}
    return render(request, 'index.html', data)

def indexfood(request):
    food2=foodCategory.objects.all()
    food3=Product.objects.all()
    # food1=fooditem.objects.all()
    data = {'food2':food2,'food3':food3}
    return render(request, 'indexfood.html', data)

def showitem(request, iid):
    
    its = item.objects.get(pk=iid)
    food2=foodCategory.objects.all()
    food3=Product.objects.all()
    
    categories = Category.objects.filter(items=its)
    data = {
        'food2':food2,
        'food3':food3,
        'categories':categories
    }
    return render(request, 'index.html',data)

def about(request):
    return render(request,'about.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            message = render_to_string('ResetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(
                'Please activate your account',
                message,
                'amusementpark521@gmail.com',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('viewlogin')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'Forgot_Password.html')
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('viewlogin')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'ResetPassword.html')

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
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register.html')



def contact(request):
    return render(request,'contact.html')

def services(request):
    return render(request,'services.html')

def packages(request):
    
        obj=Adultpackage.objects.all()
        obj2=Childpackage.objects.all()
        context={
            'obj':obj,
            'obj2':obj2
        }
        return render(request,'packages.html',context)
    

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
        request.session['email']=email
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
    return redirect('index')   

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
    return render(request, 'change.html')     

def foodregistrations(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        license=request.POST['license']
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
            reg=food_registration(username=username,phone=phone,license=license,user_id=userid.user,password=passwords)
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
    return redirect(index)    

# def foodadd(request):
#     if 'email' in request.session:

#         if request.method == 'POST':
#             brandname = request.POST.get('brandname')
#             image = request.FILES.get('image')
#             print(image)
#             food_item = fooditem(brandname=brandname, image=image)
#             food_item.save()
#             messages.success(request, 'Food item added successfully!')
#             return redirect('foodadd')
#         else:
#             return render(request, 'foodadd.html')
#     return redirect(dashboard)    

# def food_dis(request):
#     if 'email' in request.session:
#         data=fooditem.objects.all()
#         context={'data': data}
#         return render(request,'food_dis.html',context)
#     return redirect(dashboard)    
        
# def Delete(request,id):
#     if 'email' in request.session:
#         food=fooditem.objects.filter(id=id)
#         food.delete()
#         messages.info(request,"Deleted")
#         return redirect(food_dis)        
#     return redirect(dashboard)    

# def edit_food_item(request, pk):
#     if 'email' in request.session:
#         item = get_object_or_404(fooditem, pk=pk)

#         if request.method == 'POST':
#             # If the request method is POST, update the fooditem object with the new data
#             item.brandname = request.POST['brandname']
#             item.image = request.FILES['image']
#             item.save()

#             # Redirect to the fooditem detail page after editing the fooditem object
#             return redirect('food_dis')
#         else:
#             # If the request method is GET, render the edit fooditem form with the current data
#             return render(request, 'edit_food_item.html', {'item': item}) 
#     return redirect(dashboard)

def add_food_category(request):
    if 'email' in request.session:
        if request.method == 'POST':
            title = request.POST.get('title')
            category_image = request.FILES.get('category_image')
            # item_id = request.POST.get('item_id')
            if title and category_image:
                category = foodCategory.objects.create(title=title, category_image=category_image)
                return redirect('food_category_dis')
            else:
                return HttpResponseBadRequest('Title, category image, and item ID are required')
        # items = fooditem.objects.all()
        return render(request, 'add_food_category.html')   
    return redirect(dashboard)
    
def edit_food_category(request, pk):    
    if 'email' in request.session:
        category = get_object_or_404(foodCategory, pk=pk)
        if request.method == 'POST':
            title = request.POST.get('title')
            category_image = request.FILES.get('category_image')
            if title:
                category.title = title
                if category_image:
                    category.category_image = category_image
                category.save()
                return redirect('food_category_dis')
            else:
                return HttpResponseBadRequest('Title and item ID are required')
        # items = fooditem.objects.all()
        return render(request, 'edit_food_category.html', {'category': category})  
    return redirect('dashboard')



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
    if 'email' in request.session:
        category=foodCategory.objects.filter(id=id)
        category.delete()
        messages.info(request,"Deleted")
        return redirect(food_category_dis)  
    # return redirect(dashboard)
    return HttpResponse("Please Login") 




#booking

import razorpay
from datetime import datetime
@login_required
def booking(request):
    if request.method == 'POST':
        user = request.user
        p1_id = request.POST.get('p1_id')
        p2_id = request.POST.get('p2_id')
        date = request.POST.get('date')
        booking_date = datetime.strptime(date, '%Y-%m-%d')
        month = booking_date.month
        if month in [12, 1, 2]:
            season = 'Winter'
        elif month in [3, 4, 5]:
            season = 'Spring'
        elif month in [6, 7, 8]:
            season = 'Summer'
        else:
            season = 'Fall'
        print(season)
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
        booking_limit = BookingLimit.objects.filter(date=date).first()
        if booking_limit and booking_limit.max_bookings <= Book.objects.filter(date=date).count():
            messages.error(request, 'Maximum number of bookings reached for today.')
            return redirect('booking')
        elif not booking_limit:
            messages.error(request, 'Booking not available.')
            return redirect('booking')
        food_options = Product.objects.all()
        total_price = (count_adult * p1.price) + (count_child * p2.price)
        booking = Book.objects.create(user=user, p1_id=p1, p2_id=p2, date=date, count_adult=count_adult, count_child=count_child, total_price=total_price, season=season)
        # ordered_booking = Placed_Booking.objects.create(user=booking.user, p1_id=p1, p2_id=p2, date=date, count_adult=count_adult, count_child=count_child)
        # ordered_booking.save()
        food_selected = False
        for food in Product.objects.all():
            print(1)
            count = int(request.POST.get(f'food_count_{food.id}', 0))
            print(count)
            if count > 0:
                print(3)
                BookingFoodOption.objects.create(booking=booking, food_option=food, count=count)
                food_selected = True
                total_price += count * food.selling_price
                print(user, booking, food, count)
        booking.total_price = total_price  # update total price to include food cost
        booking.save()
        if food_selected:
            booking.food = True
            booking.save()
        # messages.success(request, 'Booking successful.')
        return redirect('checkout', booking.id)
    adult_packages = Adultpackage.objects.all()
    child_packages = Childpackage.objects.all()
    food_options = Product.objects.all()
    return render(request, 'booking.html', {'adult_packages': adult_packages, 'child_packages': child_packages, 'food_options': food_options})


def get_booking_limit(request):
    selected_date = request.GET.get('date')
    booking_limit = 0
    try:
        booking_limit = BookingLimit.objects.get(date=selected_date).max_bookings
    except BookingLimit.DoesNotExist:
        pass
    return JsonResponse({'booking_limit': booking_limit})

def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

def update_account(request):
    if request.method == 'POST':
        # Get the account object from the database
        account = request.user

        # Update the account object with the new data
        account.username = request.POST.get('username')
        account.email = request.POST.get('email')
        account.phone = request.POST.get('phone')
        account.save()
        
        # Return a JSON response indicating success
        return render(request,'profile.html')

    # If the request method is not POST, return an error response
    return JsonResponse({'error': 'Invalid request method'})

# def booking(request):
#     if request.method == 'POST':
#         user = request.user
#         p1_id = request.POST.get('p1_id')
#         p2_id = request.POST.get('p2_id')
#         date = request.POST.get('date')
#         booking_date = datetime.strptime(date, '%Y-%m-%d')
#         month = booking_date.month
#         if month in [12, 1, 2]:
#             season = 'Winter'
#         elif month in [3, 4, 5]:
#             season = 'Spring'
#         elif month in [6, 7, 8]:
#             season = 'Summer'
#         else:
#             season = 'Fall'
#         print(season)    
#         count_adult = int(request.POST.get('count1', 1))
#         count_child = int(request.POST.get('count2', 0))
#         try:
#             p1 = Adultpackage.objects.get(p1_id=p1_id)
#         except Adultpackage.DoesNotExist:
#             p1 = None
#         try:
#             p2 = Childpackage.objects.get(p2_id=p2_id)
#         except Childpackage.DoesNotExist:
#             p2 = None
#         if p1 is None:
#             messages.error(request, 'Invalid package selected.')
#             return redirect('booking')
#         booking_limit = BookingLimit.objects.filter(date=date).first()
#         if not booking_limit:
#             booking_limit = BookingLimit.objects.create(date=date)
#         max_bookings = booking_limit.max_bookings
#         num_bookings_today = Placed_Booking.objects.filter(date=date).count()
#         if num_bookings_today >= max_bookings:
#             messages.error(request, 'Maximum number of bookings reached for today.')
#             return redirect('booking')    
#         food_options = Product.objects.all()   
#         total_price = (count_adult * p1.price) + (count_child * p2.price)
#         booking = Book.objects.create(user=user, p1_id=p1, p2_id=p2, date=date, count_adult=count_adult, count_child=count_child, total_price=total_price,season=season)
#         # ordered_booking = Placed_Booking.objects.create(user=booking.user, p1_id=p1, p2_id=p2, date=date, count_adult=count_adult, count_child=count_child)
#         # ordered_booking.save()
#         food_selected = False
#         for food in Product.objects.all():
#             print(1)
#             count = int(request.POST.get(f'food_count_{food.id}', 0))
#             print(count)
#             if count > 0:
#                 print(3)
#                 BookingFoodOption.objects.create(booking=booking, food_option=food, count=count)
#                 food_selected = True
#                 total_price += count * food.selling_price
#                 print(user,booking, food, count)
#         if food_selected:
#             booking.food = True
#             booking.save()        
#         messages.success(request, 'Booking successful.')
#         return redirect('checkout', booking.id)
#     adult_packages = Adultpackage.objects.all()
#     child_packages = Childpackage.objects.all()
#     food_options = Product.objects.all()
#     return render(request, 'booking.html', {'adult_packages': adult_packages, 'child_packages': child_packages,'food_options': food_options})

from django.db.models import Q
@login_required 
@login_required 
def checkout(request, booking_id):
    latest_booking = Book.objects.get(id=booking_id)
    active_offers = Offer.objects.filter(active=True)
    booking_food_options = latest_booking.bookingfoodoption_set.all()
    applied_offers_count = 0
    eligible_offers = []
    discount = 0
    
    for offer in active_offers:
        if offer.count_adult is not None and latest_booking.count_adult >= offer.count_adult:
            adult_offers = active_offers.filter(count_adult__lte=latest_booking.count_adult)
            for adult_offer in adult_offers:
                if adult_offer not in eligible_offers:
                    eligible_offers.append(adult_offer)
                    applied_offers_count += 1
        if offer.count_child is not None and latest_booking.count_child >= offer.count_child:
            child_offers = active_offers.filter(count_child__lte=latest_booking.count_child)
            for child_offer in child_offers:
                if child_offer not in eligible_offers:
                    eligible_offers.append(child_offer)
                    applied_offers_count += 1

    for offer in eligible_offers:
        discount += (latest_booking.total_price * offer.discount_percentage) / 100

    latest_booking.applied_offers = applied_offers_count
    latest_booking.discount_amount = discount
    latest_booking.total_price = int(latest_booking.total_price - discount)

    if 'discount_applied' not in request.session:
        request.session['discount_applied'] = True

    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
    data = {
        'amount': latest_booking.total_price * 100,  
        'currency': 'INR',
        'receipt': str(latest_booking.id),
        'payment_capture': 1,
    }
    order = client.order.create(data=data)
    order_id = order['id']
    print(order_id)
    request.session['order_id'] = order_id
    print(order_id)
    request.session['booking_id'] = booking_id
    order_status = order['status']
    if order_status == 'created':
        payment = Payments.objects.create(
            user=latest_booking.user,
            amount=latest_booking.total_price,
            razorpay_order_id=order_id,
            razorpay_payment_status=order_status,
        )
        latest_booking.payment = payment
        latest_booking.save()
    context = {
        'booking_food_options': booking_food_options,
        'latest_booking': latest_booking,
        'eligible_offers': eligible_offers,
        'order_id': order_id
    }

    return render(request, 'checkout.html', context)





# def checkout(request, booking_id):
#     latest_booking = Book.objects.get(id=booking_id)
#     active_offers = Offer.objects.filter(active=True)
#     booking_food_options = latest_booking.bookingfoodoption_set.all()
#     applied_offers_count = 0
#     eligible_offers = []
#     for offer in active_offers:
#         if offer.count_adult is not None and latest_booking.count_adult >= offer.count_adult:
#             adult_offers = active_offers.filter(count_adult__lte=latest_booking.count_adult)
#             for adult_offer in adult_offers:
#                 if adult_offer not in eligible_offers:
#                     eligible_offers.append(adult_offer)
#                     applied_offers_count += 1
#         if offer.count_child is not None and latest_booking.count_child >= offer.count_child:
#             child_offers = active_offers.filter(count_child__lte=latest_booking.count_child)
#             for child_offer in child_offers:
#                 if child_offer not in eligible_offers:
#                     eligible_offers.append(child_offer)
#                     applied_offers_count += 1

#     for offer in eligible_offers:
#         discount = (latest_booking.total_price * offer.discount_percentage) / 100
#         latest_booking.total_price -= discount

#     latest_booking.applied_offers = applied_offers_count
#     latest_booking.total_price = int(latest_booking.total_price)

#     if 'discount_applied' not in request.session:
#         request.session['discount_applied'] = True

#     client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
#     data = {
#         'amount': latest_booking.total_price * 100,  
#         'currency': 'INR',
#         'receipt': str(latest_booking.id),
#         'payment_capture': 1,
#     }
#     order = client.order.create(data=data)
#     order_id = order['id']
#     print(order_id)
#     request.session['order_id'] = order_id
#     print(order_id)
#     request.session['booking_id'] = booking_id
#     order_status = order['status']
#     if order_status == 'created':
#         payment = Payments.objects.create(
#             user=latest_booking.user,
#             amount=latest_booking.total_price,
#             razorpay_order_id=order_id,
#             razorpay_payment_status=order_status,
#         )
#         latest_booking.payment = payment
#         latest_booking.save()
#         # return render(request,'success.html')

#     context = {
#         'booking_food_options': booking_food_options,
#         'latest_booking': latest_booking,
#         'eligible_offers': eligible_offers,
#         'order_id': order_id
#     }

#     return render(request, 'checkout.html', context)

@login_required
def paymentdone(request):
    # if request.method == 'POST':
        urls=request.META.get('HTTP_REFERER')
        payment=''
        if request.GET.get('payment_id') :
            payment_id = request.GET.get('payment_id', None)
            print(payment_id)
            payment = Payments.objects.get(razorpay_order_id=request.session['order_id'])
            payment.razorpay_payment_id=payment_id
            payment.paid=True
            payment.save()
            booking_id = request.session['booking_id']
            booking = Book.objects.get(id=booking_id)
            ordered_booking=Placed_Booking.objects.create(
                user=booking.user,
                p1_id=booking.p1_id,
                p2_id=booking.p2_id,
                date=booking.date,
                count_adult=booking.count_adult,
                count_child=booking.count_child,
                food=booking.food,
                total_price=booking.total_price,
                paid=True
            )
            ordered_booking.save()
            return render(request,'paymentdone.html')
        return redirect(booking)

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from .utils import TicketPDF

from django.contrib.auth.decorators import login_required
@login_required
def download_ticket(request):
    user = request.user
    booking = Book.objects.filter(user=request.user).latest('created_at')
    adult_count = booking.count_adult
    child_count = booking.count_child
    Package_Adult = booking.p1_id
    Package_Child = booking.p2_id

    # ticket_type = 'Adult' if booking.p1_id == 'A' else 'Child'
    date = booking.date
    total_price = booking.total_price

    ticket_details = {
        'Package_Adult': Package_Adult,
        'Package_Child': Package_Child,
        'date': date,
        'total_price': total_price,
        'adult_count': adult_count,
        'child_count': child_count,
    }
    
    # Get the food options for the current booking
    food_options = BookingFoodOption.objects.filter(booking=booking)

    ticket_pdf = TicketPDF(adult_count=adult_count, child_count=child_count)
    ticket_pdf.set_ticket_details(ticket_details)
    
    # Add the food options to the PDF
    ticket_pdf.set_food_options(food_options)
    
    ticket_data = ticket_pdf.get_pdf_bytes()

    response = HttpResponse(ticket_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; ticket.pdf'

    return response




def item_add(request):
    if 'email' in request.session:
        if request.method == 'POST':
            name = request.POST.get('name')
            product_image = request.FILES.get('product_image')
            cat = request.POST.get('cat')
            selling_price = request.POST.get('selling_price')
            cat = get_object_or_404(foodCategory, pk=cat)
            # brand =get_object_or_404(fooditem, pk=brand)
            if name and product_image and cat:
                product = Product.objects.create(name=name, product_image=product_image, cat=cat , selling_price=selling_price)
                messages.success(request,"Added Successfully")
                return redirect('item_view')
            else:
                return HttpResponseBadRequest('Name, image, and category are required')
        else:
            categories = foodCategory.objects.all()
            # obj = fooditem.objects.all()
            return render(request, 'item_add.html', {'items': categories})
    return redirect(dashboard)

def item_view(request):
    if 'email' in request.session:
        data=Product.objects.all()
        context={'data': data}
        return render(request,'item_view.html',context)
    return redirect(dashboard)

def delete_item_view(request,id):
    if 'email' in request.session:
        category=Product.objects.filter(id=id)
        category.delete()
        messages.info(request,"Deleted")
        return redirect(item_view)  
    return HttpResponse("Please Login") 

def edit_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        product_image = request.FILES.get('product_image')
        cat_id = request.POST.get('cat')
        selling_price = request.POST.get('selling_price')
        cat = get_object_or_404(foodCategory, pk=cat_id)
        if name and cat:
            product.name = name
            if product_image:
                product.product_image = product_image
            product.cat = cat
            product.selling_price = selling_price
            product.save()
            return redirect('item_view')
        else:
            return HttpResponseBadRequest('Name and category are required')
    else:
        categories = foodCategory.objects.all()
        return render(request, 'edit_item.html', {'product': product, 'categories': categories})


from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
def booked_food(request):
    today = timezone.now().date() # get today's date in timezone
    bookings_today = Book.objects.filter(date__exact=today, food=True) # filter only food bookings
    query = None
    if request.method == 'GET':
        query = request.GET.get('q')
        print(query)
        if query:
            bookings_today = bookings_today.filter(Q(user__email__icontains=query) | Q(id__icontains=query))
    context = {
        'booked_today': bookings_today,
        'query': query,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('booked_food_ajax.html', context)
        data_dict = {'html_from_view': html}
        return JsonResponse(data=data_dict)
    return render(request, 'booked_food.html', context)



from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(request, booking_id):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    booking = Book.objects.get(id=booking_id)
    food_options = BookingFoodOption.objects.filter(booking=booking) 
    logo_path = r'C:\Users\lenovo\amusementpark\AmusementPark\static\images\logo2.jpg'
    p.drawImage(logo_path, 50, 750, width=100, height=100)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 780, "DreamlandPark")    
    p.setFont("Helvetica", 12)
    p.rect(90, 500, 400, 200)
    p.drawString(200, 720, "Food Details:")
    y = 680
    for food_option in food_options:
        name = food_option.food_option.name
        category = food_option.food_option.cat.title
        count = str(food_option.count)
        status = "Served" if food_option.served else "Not Served"
        p.drawString(100, y, name)
        p.drawString(200, y, category)
        p.drawString(300, y, count)
        p.drawString(400, y, status)
        y -= 20
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="food_details_{booking_id}.pdf"'
    response.write(pdf)
    return response

def food_details(request, booking_id):
    if 'email' in request.session:
        booking = Book.objects.get(id=booking_id)
        food_options = BookingFoodOption.objects.filter(booking=booking)
        context = {'booking': booking, 'food_options': food_options}
        pdf_url = reverse('generate_pdf', kwargs={'booking_id': booking_id})
        context['pdf_url'] = pdf_url
        return render(request, 'food_details.html', context)
    else:
        return JsonResponse({'success': False})


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def serve_food_option(request):
    if 'email' in request.session:
        booking_food_option_id = request.POST.get('booking_food_option_id')
        if booking_food_option_id:
            booking_food_option = get_object_or_404(BookingFoodOption, id=booking_food_option_id)
            booking_food_option.served = True
            booking_food_option.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid booking food option ID.'})
    else:
        return JsonResponse({'success': False, 'message': 'User is not authenticated.'})

def food_option_display(request):
    if 'email' in request.session:
        booking_food_options = BookingFoodOption.objects.all()
        return render(request, 'food_option_display.html', {'booking_food_options': booking_food_options})
    
    return redirect('index')


from django.shortcuts import render
from django.db.models import Sum
from .models import BookingFoodOption
def food_count(request):
    if request.method == 'POST':
        date = request.POST['selected_date']
        food_bookings = Book.objects.filter(date=date, food=True)
        food_options = BookingFoodOption.objects.filter(booking__in=food_bookings).values('food_option__name', 'food_option__cat__title').annotate(count=Sum('count'))
        context = {
            'date': date,
            'food_options': food_options
        }
        return render(request, 'food_count.html', context)
    return render(request, 'food_count.html')

#foodchart
from django.db.models import Sum
from .models import BookingFoodOption

import random

def sales_chart(request):
    sales_data = BookingFoodOption.objects.values('food_option__name').annotate(total_sales=Sum('count'))
    labels = []
    data = []
    colors = []
    for item in sales_data:
        labels.append(item['food_option__name'])
        data.append(item['total_sales'])
        colors.append('#%06X' % random.randint(0, 0xFFFFFF))
    context = {
        'labels': labels,
        'data': data,
        'colors': colors,
    }
    return render(request, 'dashboard.html', context)

    

def dashboard(request):
    if 'email' in request.session:
        email=request.session['email']
        # get sales data for chart
        sales_data = BookingFoodOption.objects.values('food_option__name').annotate(total_sales=Sum('count'))
        labels = []
        data = []
        colors = []
        for item in sales_data:
            labels.append(item['food_option__name'])
            data.append(item['total_sales'])
            colors.append('#%06X' % random.randint(0, 0xFFFFFF))
        chart_data = {
            'labels': labels,
            'data': data,
            'colors': colors,
        }
        # render dashboard template with chart data
        return render(request,'dashboard.html', {'chart_data': chart_data})




#filtering
from django.shortcuts import render
from .models import BookingFoodOption

def booking_food_options(request):
    served = request.GET.get('served', '')
    if served:
        booking_food_options = BookingFoodOption.objects.filter(served=(served == 'yes'))
    else:
        booking_food_options = BookingFoodOption.objects.all()

    context = {
        'booking_food_options': booking_food_options,
    }
    return render(request, 'food_option_display.html', context)

def search_booking_food_options(request):
    search_value = request.GET.get('search_value', '')
    booking_id = request.GET.get('booking_id', '')
    email = request.GET.get('email', '')
    date = request.GET.get('date', '')
    
    results = BookingFoodOption.objects.filter(
        Q(booking__user__email__icontains=search_value) | 
        Q(booking__date__icontains=search_value) |
        Q(booking__id__icontains=booking_id) |
        Q(booking__user__email__icontains=email) |
        Q(booking__date__icontains=date) |
        Q(food_option__name__icontains=search_value)
    )
    
    search_results = []
    for result in results:
        search_results.append({
            'booking_id': result.booking_id,
            'booking': result.booking.user.email,
            'booking_date': result.booking.date,
            'food_option': result.food_option.name,
            'count': result.count,
            'served': result.served
        })
    return JsonResponse({'results': search_results})



def create_review(request):
    if request.method == 'POST':
        user = request.user
        print(user)
        review_text = request.POST['review_text']
        print(review_text)
        rating = request.POST['rating']
        print(rating)
        reviews = review(user=user, review_text=review_text, rating=rating)
        reviews.save()
        print(reviews)
        messages.success(request,"Review successfully added")
        return redirect('create_review')
    return render(request, 'review.html')

#ml
import pickle
from django.shortcuts import render
from django.http import JsonResponse
@login_required
def home(request):
    if request.method == 'POST':
        season = request.POST.get('season')
        offers = float(request.POST.get('offers'))
        with open('predict.pkl', 'rb') as f:
            model = pickle.load(f)
        if season == 'Spring':
            season_spring = 1
            season_summer = 0
            season_fall = 0
            season_winter = 0
        elif season == 'Summer':
            season_spring = 0
            season_summer = 1
            season_fall = 0
            season_winter = 0   
        elif season == 'Fall':
            season_spring = 0
            season_summer = 0
            season_fall = 1
            season_winter = 0
        else:
            season_spring = 0
            season_summer = 0
            season_fall = 0
            season_winter = 1
        print(season)
        prediction = round(model.predict([[season_spring, season_summer, season_fall, season_winter, offers]])[0],)    
        return render(request, 'home.html', {'season':season ,'prediction': prediction})
    return render(request, 'home.html')

    

@login_required
def offers_by_season(request):
    predicts = predict.objects.all()
    df = pd.DataFrame(list(predicts.values()))
    df['visitors'] = df['count_adult'] + df['count_child']
    offers_df = df[['season', 'visitors', 'offers']]
    offers_sum_df = offers_df.groupby('season')['offers'].sum()
    labels = offers_sum_df.index.tolist()
    values = offers_sum_df.values.tolist()
    chart_data = {'labels': labels, 'values': values}
    return render(request, 'chart.html', {'chart_data': chart_data})

