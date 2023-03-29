from django.urls import path, include
from amuzeapp import views
from .views import*
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
# from prediction.views import home
# from .admin import custom_admin_site

from django.urls import path
from . import views, admin
from django.urls import path
# from .views import download_ticket


urlpatterns = [
    # path('admin/', custom_admin_site.urls),
    path('',views.index,name='index'),
    path('home/', views.home, name='home'),
    path('result/', views.result, name='result'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('services/',views.services,name='services'),
    path('packages/',views.packages,name='packages'),
    path('viewlogin/',views.viewlogin,name='viewlogin'),
    path('register/',views.register,name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('viewlogin/',views.viewlogin,name='viewlogin'),
    path('logout/',views.logout,name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('item/<int:iid>/', views.showitem, name='item'),
    # path('category/<int:cid>/', views.showcategory, name='category'),
    path('foodlogin/',views.foodlogin,name='foodlogin'),
    path('foodregistrations/',views.foodregistrations,name='foodregistrations'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('foodlogout/',views.foodlogout,name='foodlogout'),
    path('foodadd/',views.foodadd,name='foodadd'),
    path('item_add/',views.item_add,name='item_add'),
    path('food_dis/', views.food_dis, name='food_dis'),
    path('Delete/<int:id>/',views.Delete,name='Delete'),
    path('fooditem/<int:pk>/edit/', edit_food_item, name='edit_food_item'),
    path('add_food_category/', views.add_food_category, name='add_food_category'),
    path('food_category_dis/', views.food_category_dis, name='food_category_dis'),
    path('edit_food_category/<int:pk>/', views.edit_food_category, name='edit_food_category'),
    path('delete_food_category/<int:id>/',views.delete_food_category,name='delete_food_category'),
    path('booking/', views.booking, name='booking'),
    path('paymentdone', views.paymentdone, name='paymentdone'),
    path('checkout/<int:booking_id>/', checkout, name='checkout'),
    path('item_view/', views.item_view, name='item_view'),
    path('delete_item_view/<int:id>/',views.delete_item_view,name='delete_item_view'),
    path('edit_item/<int:pk>/', views.edit_item, name='edit_item'),
    path('indexfood/', views.indexfood, name='indexfood'),
    path('booked_food/', views.booked_food, name='booked_food'),
    path('food_details/<int:booking_id>/', views.food_details, name='food_details'),
    path('serve_food_option/', views.serve_food_option, name='serve_food_option'),
    path('food_option_display/', views.food_option_display, name='food_option_display'),
    path('download_ticket', views.download_ticket, name='download_ticket'),
    # path('ticket', views.ticket, name='ticket'),



]

