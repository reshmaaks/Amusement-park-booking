# import json
# from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from hashlib import sha256
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
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
    food1=fooditem.objects.all()
    food2=foodCategory.objects.all()
    food3=Product.objects.all()
    data = {'product':product, 'categories':categories,'itms':itms ,'food1':food1,'food2':food2,'food3':food3}
    return render(request, 'index.html', data)

def indexfood(request):
    food2=foodCategory.objects.all()
    food3=Product.objects.all()
    food1=fooditem.objects.all()
    data = {'food1':food1,'food2':food2,'food3':food3}
    return render(request, 'indexfood.html', data)

def showitem(request, iid):
    
    its = item.objects.get(pk=iid)
    food2=foodCategory.objects.all()
    food3=Product.objects.all()
    food1=fooditem.objects.all()
    categories = Category.objects.filter(items=its)
    data = {
        'food1':food1,
        'food2':food2,
        'food3':food3,
        'categories':categories
    }
    return render(request, 'index.html',data)

# def showcategory(request, cid):
#     categories = Category.objects.all()
#     # obj = Deals.objects.all()
#     cats = Category.objects.get(pk=cid)
#     product = Product.objects.filter(cat=cats)
#     data = {
#         # 'categories':categories,
#         # 'result': obj,
#         'product': product
#     }
#     return render(request, 'index.html', data)
    
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
    return render(request, 'change_password.html')     

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

def foodadd(request):
    if 'email' in request.session:

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
    return redirect(dashboard)    

def food_dis(request):
    if 'email' in request.session:
        data=fooditem.objects.all()
        context={'data': data}
        return render(request,'food_dis.html',context)
    return redirect(dashboard)    
        
def Delete(request,id):
    if 'email' in request.session:
        food=fooditem.objects.filter(id=id)
        food.delete()
        messages.info(request,"Deleted")
        return redirect(food_dis)        
    return redirect(dashboard)    

def edit_food_item(request, pk):
    if 'email' in request.session:
        item = get_object_or_404(fooditem, pk=pk)

        if request.method == 'POST':
            # If the request method is POST, update the fooditem object with the new data
            item.brandname = request.POST['brandname']
            item.image = request.FILES['image']
            item.save()

            # Redirect to the fooditem detail page after editing the fooditem object
            return redirect('food_dis')
        else:
            # If the request method is GET, render the edit fooditem form with the current data
            return render(request, 'edit_food_item.html', {'item': item}) 
    return redirect(dashboard)

def add_food_category(request):
    if 'email' in request.session:
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
    return redirect(dashboard)
    
def edit_food_category(request, pk):    
    if 'email' in request.session:
        category = get_object_or_404(foodCategory, pk=pk)
        if request.method == 'POST':
            title = request.POST.get('title')
            category_image = request.FILES.get('category_image')
            item_id = request.POST.get('item_id')
            if title and item_id:
                item_instance = get_object_or_404(fooditem, pk=item_id)
                category.title = title
                if category_image:
                    category.category_image = category_image
                category.items = item_instance
                category.save()
                return redirect('food_category_dis')
            else:
                return HttpResponseBadRequest('Title and item ID are required')
        items = fooditem.objects.all()
        return render(request, 'edit_food_category.html', {'category': category, 'items': items})  
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

@login_required(login_url='viewlogin')
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
        booking_limit = BookingLimit.objects.first()
        max_bookings = booking_limit.max_bookings
        num_bookings_today = Book.objects.filter(date=date).count()
        if num_bookings_today >= max_bookings:
            messages.error(request, 'Maximum number of bookings reached for today.')
            return redirect('booking')    
        food_options = Product.objects.all()   
        total_price = (count_adult * p1.price) + (count_child * p2.price)
        booking = Book.objects.create(user=user, p1_id=p1, p2_id=p2, date=date, count_adult=count_adult, count_child=count_child, total_price=total_price,season=season)
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
                print(user,booking, food, count)
        if food_selected:
            booking.food = True
            booking.save()        
        messages.success(request, 'Booking successful.')
        return redirect('checkout', booking.id)
    adult_packages = Adultpackage.objects.all()
    child_packages = Childpackage.objects.all()
    food_options = Product.objects.all()
    return render(request, 'booking.html', {'adult_packages': adult_packages, 'child_packages': child_packages,'food_options': food_options})

from django.db.models import Q

@login_required(login_url='viewlogin') 
def checkout(request, booking_id):
    latest_booking = Book.objects.get(id=booking_id)
    active_offers = Offer.objects.filter(active=True)
    booking_food_options = latest_booking.bookingfoodoption_set.all()
    applied_offers_count = 0
    eligible_offers = []
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
    if 'discount_applied' not in request.session:
        for offer in eligible_offers:
            discount = (latest_booking.total_price * offer.discount_percentage) / 100
            latest_booking.total_price -= discount
        request.session['discount_applied'] = True
        # print(offer.discount_percentage)
    print(offer.discount_percentage)
    pred=predict.objects.create(season=latest_booking.season,count_adult=latest_booking.count_adult,count_child=latest_booking.count_child,offers=offer.discount_percentage)
    # pred=predict.objects.create(offers=offer.discount_percentage)
    pred.save()    
    latest_booking.applied_offers = applied_offers_count
    latest_booking.total_price = int(latest_booking.total_price)

    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
    data = {
        'amount': latest_booking.total_price * 100,  # Convert to paise
        'currency': 'INR',
        'receipt': str(latest_booking.id),
        'payment_capture': 1,
    }
    order = client.order.create(data=data)
    order_id = order['id']
    print(order_id)
    request.session['order_id'] = order_id
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
        # return render(request,'success.html')

    context = {
        'booking_food_options': booking_food_options,
        'latest_booking': latest_booking,
        'eligible_offers': eligible_offers,
        'order_id': order_id
    }

    return render(request, 'checkout.html', context)



@login_required(login_url='login')
def paymentdone(request):
    urls=request.META.get('HTTP_REFERER')
    payment=''
    if request.GET.get('payment_id') :
        payment_id = request.GET.get('payment_id', None)
        print(payment_id)
        payment=Payments.objects.get(razorpay_order_id=request.session['order_id'])
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
            total_price=booking.total_price,
            paid=True
        )
        ordered_booking.save()
        return render(request,'paymentdone.html')
    return redirect(booking)


def item_add(request):
    if 'email' in request.session:
        if request.method == 'POST':
            name = request.POST.get('name')
            product_image = request.FILES.get('product_image')
            cat = request.POST.get('cat')
            brand = request.POST.get('brand')

            selling_price = request.POST.get('selling_price')
            cat = get_object_or_404(foodCategory, pk=cat)
            brand =get_object_or_404(fooditem, pk=brand)
            if name and product_image and cat:
                product = Product.objects.create(name=name, product_image=product_image, cat=cat,brand=brand, selling_price=selling_price)
                messages.success(request,"Added Successfully")

                return redirect('item_view')
            else:
                return HttpResponseBadRequest('Name, image, and category are required')
        else:
            categories = foodCategory.objects.all()
            obj = fooditem.objects.all()

            return render(request, 'item_add.html', {'obj':obj, 'items': categories})
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
    # return redirect(dashboard)
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

def booked_food(request):
    today = timezone.now().date() # get today's date in timezone
    bookings_today = Book.objects.filter(date__exact=today, food=True) # filter only food bookings
    context = {
        'booked_today': bookings_today
    }
    return render(request, 'booked_food.html', context)


def food_details(request, booking_id):
    if 'email' in request.session:
        booking = Book.objects.get(id=booking_id)
        food_options = BookingFoodOption.objects.filter(booking=booking)
        return render(request, 'food_details.html', {'food_options': food_options})
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
@login_required

def food_option_display(request):
    if 'email' in request.session:
        booking_food_options = BookingFoodOption.objects.all()
        return render(request, 'food_option_display.html', {'booking_food_options': booking_food_options})
    else:
        return redirect('login')

from django.shortcuts import render
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression


# # csv_path = r'C:\Users\lenovo\predictions\predict\predict.csv'
# # # Load the amusement park dataset
# # df = pd.read_csv(csv_path)

# # # Convert categorical variables to numerical variables
# # df = pd.get_dummies(df, columns=['Season'])

# # X = df.drop('Num_Customers', axis=1)
# # y = df['Num_Customers']
# # model = LinearRegression()
# # model.fit(X, y)

# def home(request):
#     model=pickle.load(open('predict.pkl','rb'))
#     data=pd.read_csv('predict.csv')
#     if request.method == 'POST':
#         # Get the form data
#         season = request.POST['season']
#         offers = request.POST['offers']
#         print(1)
#         # Convert the categorical variable to numerical variable
#         if season == 'Spring':
#             print(2)
#             season_spring = 1
#             season_summer = 0
#             season_fall = 0
#             season_winter = 0
#         elif season == 'Summer':
#             season_spring = 0
#             season_summer = 1
#             season_fall = 0
#             season_winter = 0
#         elif season == 'Fall':
#             season_spring = 0
#             season_summer = 0
#             season_fall = 1
#             season_winter = 0
#         else:
#             season_spring = 0
#             season_summer = 0
#             season_fall = 0
#             season_winter = 1
        
#         # Make a prediction using the trained model
#         # prediction = round(model.predict([[season_spring, season_summer, season_fall, season_winter, offers]])[0],)
#         prediction=model.predict(pd.DataFrame(columns=['season','offers'],data=[[season,offers]]))
        
#         # Render the result template with the prediction
#         return render(request, 'result.html', {'season':season ,'offers':offers,'prediction': prediction})
        
#     else:
#         # Render the home template
#         return render(request, 'home.html')
# def result(request,prediction):
#     return render(request, 'result.html', {'prediction': prediction})

import pickle
from django.shortcuts import render
from django.http import JsonResponse

# define the path to the pickle file
# PICKLE_FILE = '/content/drive/My Drive/Colab Notebooks/predict.pkl'

def home(request):
    if request.method == 'POST':
        # extract the input data from the request
        season = request.POST.get('season')
        offers = float(request.POST.get('offers'))
        
        # load the trained model from the pickle file
        with open('predict.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # convert the season variable to one-hot encoded values
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
        
        # make a prediction using the trained model
        prediction = round(model.predict([[season_spring, season_summer, season_fall, season_winter, offers]])[0],)    
        
        # return the prediction as a JSON response
        return render(request, 'home.html', {'prediction': prediction})
    
    # if the request method is not POST, render the template with a form
    return render(request, 'home.html')

def result(request,prediction):
    return render(request, 'result.html', {'prediction': prediction})





from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from io import BytesIO
from .utils import TicketPDF
def download_ticket(request):
    booking = Book.objects.first()  # Get the first booking instance
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
    
    ticket_pdf = TicketPDF(adult_count=adult_count, child_count=child_count)
    ticket_pdf.set_ticket_details(ticket_details)
    ticket_data = ticket_pdf.get_pdf_bytes()

    response = HttpResponse(ticket_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; ticket.pdf'

    return response
# import os
# import sys

# sys.path.append(os.path.abspath(r"c:\users\lenovo\amusementpark\env\lib\site-packages"))

# from django.template.loader import get_template
# from xhtml2pdf import pisa


# def pdf_report_create(request):
#     # products = Product.objects.all()
#     template_path = 'ticket.html'
#     context = {}
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="products_report.pdf"'
#     template = get_template(template_path)
#     html = template.render(context)
#     pisa_status = pisa.CreatePDF(
#        html, dest=response)
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response


# def ticket(request):
#     return render(request,ticket.html)
