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
    path('fooddis/', views.fooddis, name='fooddis'),
    path('Delete/<int:id>/',views.Delete,name='Delete'),
    path('fooditem/<int:pk>/edit/', edit_food_item, name='edit_food_item'),
    path('add_food_category/', views.add_food_category, name='add_food_category'),
    path('food_category_dis/', views.food_category_dis, name='food_category_dis'),
    path('edit_food_category/<int:pk>/', views.edit_food_category, name='edit_food_category'),
    path('delete_food_category/<int:id>/',views.delete_food_category,name='delete_food_category'),








    

]    