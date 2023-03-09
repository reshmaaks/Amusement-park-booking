from django.urls import path, include
from amuzeapp import views
from .views import*
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.index,name='index'),
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
    path('category/<int:cid>/', views.showcategory, name='category'),
    path('foodlogin/',views.foodlogin,name='foodlogin'),
    path('foodregistrations/',views.foodregistrations,name='foodregistrations'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('foodlogout/',views.foodlogout,name='foodlogout'),
    path('foodadd/',views.foodadd,name='foodadd'),
    path('fooddis/',views.fooddis,name='fooddis'),





    

]    