from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin

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



class Product(models.Model):
    name = models.CharField(max_length=200,unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='media')
    # marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField(null=True)
    # stock=models.IntegerField(default=True)

    def __str__(self):
        return self.name



class fooditem(models.Model):
    brandname = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='media/cat-photo')
    def __str__(self):
        return self.brandname       

class foodCategory(models.Model):
    title = models.CharField(max_length=200,unique=True)
    items=models.ForeignKey(fooditem,on_delete=models.CASCADE,null=True)
    category_image = models.ImageField(upload_to='media/f-photo')

    def __str__(self):
        return self.title    

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
        
class Reviews(models.Model):
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
    order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)  
    def __str__(self):
        return self.user      

class Placed_Booking(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    # booking=models.ForeignKey(booking,on_delete=models.CASCADE,null=True,blank=True)
    p1_id=models.ForeignKey(Adultpackage,on_delete=models.CASCADE,null=True,blank=True)
    p2_id=models.ForeignKey(Childpackage,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    payment=models.ForeignKey(Payments,on_delete=models.CASCADE,default="")
    def __str__(self):
        return self.user