from os import path
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin
from sklearn import model_selection

class MyAccountManager(BaseUserManager):
    def create_user(self, username, email,phone, password=None):   
        
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
           
            phone = phone,
            # is_superuser=is_superuser,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, password, email, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password, **extra_fields
            )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    

class Account(AbstractBaseUser,PermissionsMixin):
    
   
    # role_choices    =(('is_admin','is_admin'),('is_superadmin','is_superadmin'),('None','None'))
    id              = models.AutoField(primary_key=True)
    username        = models.CharField(max_length=100, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone           = models.BigIntegerField(default=0)
    is_superuser   = models.BooleanField(default=False)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_staff        = models.BooleanField(default=False)
    is_admin        =models.BooleanField(default=False)
    is_active        =models.BooleanField(default=False)
    # is_superuser   = models.BooleanField(default=False)

    objects = MyAccountManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone']
   

    class Meta:
        db_table="home_account"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin




#foodcourt
class food_login(models.Model):
    user = models.EmailField(max_length=200, unique=True, primary_key=True,default=1)
    password = models.CharField(max_length=100)
    type=models.BooleanField(max_length=100,default=False)
    def __str__(self):
        return str(self.user) 

class food_registration(models.Model):
    username = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    license=models.CharField(max_length=200,unique=True,null=True)

    user = models.ForeignKey(food_login, on_delete=models.SET_NULL, blank=True, null=True)
    password = models.CharField(max_length=100)
    def __str__(self):
        return str(self.username) 



class item(models.Model):
    item = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='item-photo',null=True)

    def __str__(self):
        return self.item

class Category(models.Model):
    title = models.CharField(max_length=200,unique=True)
    items=models.ForeignKey(item,on_delete=models.CASCADE,null=True)
    # descripsion = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to='cat-photo')

    def __str__(self):
        return self.title

class fooditem(models.Model):
    brandname = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='media/cat-photo')
    def __str__(self):
        return self.brandname       

class foodCategory(models.Model):
    title = models.CharField(max_length=200,unique=True)
    # items=models.ForeignKey(fooditem,on_delete=models.CASCADE,null=True)
    category_image = models.ImageField(upload_to='media/f-photo')

    def __str__(self):
        return self.title    

class Product(models.Model):
    name = models.CharField(max_length=200,unique=True)
    cat = models.ForeignKey(foodCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(fooditem,on_delete=models.CASCADE,null=True)
    product_image = models.ImageField(upload_to='media/p-image')
    # marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField(null=True)
    # stock=models.IntegerField(default=True)

    def __str__(self):
        return self.name        

class Adultpackage(models.Model):
    p1_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    price=models.BigIntegerField(default=0)
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.name)


class Childpackage(models.Model):
    p2_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    price=models.BigIntegerField(default=0)
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.name)        
        
class Review(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    review = models.CharField(max_length=500, blank=True)
    # image= models.ImageField(upload_to='reviews/',blank=True,default=True)
    star =models.IntegerField(default=False)


    def _str_(self):
        return str(self.user)



class Payments(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    # name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_status=models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True,null=True)
    paid = models.BooleanField(default=False)  
    def __str__(self):
        return self.user      

class Placed_Booking(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    p1_id=models.ForeignKey(Adultpackage,on_delete=models.CASCADE,null=True,blank=True)
    p2_id=models.ForeignKey(Childpackage,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    count_adult=models.BigIntegerField(default=1)
    count_child=models.BigIntegerField(default=1,null=True)
    total_price=models.BigIntegerField(default=0)
    paid = models.BooleanField(default=False, null=True)
    def __str__(self):
        return self.user



class Book(models.Model):
    SEASON_CHOICES = [
    ('Winter', 'Winter'),
    ('Spring', 'Spring'),
    ('Summer', 'Summer'),
    ('Fall', 'Fall')
    ]

    season = models.CharField(max_length=20, choices=SEASON_CHOICES, null=True, blank=True)
    user =models.ForeignKey(Account, on_delete=models.SET_NULL,null=True)
    p1_id=models.ForeignKey(Adultpackage,on_delete=models.CASCADE,null=True,blank=True)
    p2_id=models.ForeignKey(Childpackage,on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(auto_now = False)
    count_adult=models.BigIntegerField(default=1)
    count_child=models.BigIntegerField(default=1,null=True)
    total_price=models.BigIntegerField(default=0)
    food = models.BooleanField(default=False,null=True)
    applied_offers = models.IntegerField(default=0,null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user) 
               
class BookingFoodOption(models.Model):
    booking = models.ForeignKey(Book, on_delete=models.CASCADE)
    food_option = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    served = models.BooleanField(default=False) 
    def __str__(self):
        return f"{self.count} x {self.food_option.name} ({self.booking.user.username})"


class Offer(models.Model):
    name = models.CharField(max_length=255)
    discount_percentage = models.IntegerField()
    active = models.BooleanField(default=True)
    count_adult = models.PositiveIntegerField(null=True)
    count_child = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name        

class BookingLimit(models.Model):

    max_bookings = models.PositiveIntegerField(default=True)

# from django.shortcuts import render,redirect
# from django.contrib import admin

# class Prediction(admin.ModelAdmin):
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('predict/', self.predict_view, name='predict'),
#         ]
#         return custom_urls + urls
#     def predict_view(request):
#             if request.method == 'POST':
#                 # Get the form data
#                 season = request.POST['season']
#                 offers = request.POST['offers']
                
#                 # Convert the categorical variable to numerical variable
#                 if season == 'Spring':
#                     season_spring = 1
#                     season_summer = 0
#                     season_fall = 0
#                     season_winter = 0
#                 elif season == 'Summer':
#                     season_spring = 0
#                     season_summer = 1
#                     season_fall = 0
#                     season_winter = 0
#                 elif season == 'Fall':
#                     season_spring = 0
#                     season_summer = 0
#                     season_fall = 1
#                     season_winter = 0
#                 else:
#                     season_spring = 0
#                     season_summer = 0
#                     season_fall = 0
#                     season_winter = 1
                
#                 # Make a prediction using the trained model
#                 prediction = round(model_selection.predict([[season_spring, season_summer, season_fall, season_winter, offers]])[0],)
                
#                 # Render the result template with the prediction
#                 return render(request, 'result.html', {'season':season ,'offers':offers,'prediction': prediction})
                
#             else:
#                 # Render the home template
#                 return render(request, 'home.html')
