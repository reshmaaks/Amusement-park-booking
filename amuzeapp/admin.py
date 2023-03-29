import csv
from os import path
# from .views import home
# admin.site.register.urls(home)
from django.contrib import admin
from django.http import HttpResponse
from sklearn import model_selection
from.models import *
from django.contrib.auth.models import Group
# Register your models here.
# from django.shortcuts import render,redirect

# from django.contrib import admin
# from django.urls import reverse
# from django.utils.html import format_html
# from .models import Prediction
# from .models import  Offer

# class PredictionAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(Prediction, PredictionAdmin)
# admin.site.register(Prediction)
# admin.site.register(/home)

admin.site.unregister(Group)

admin.site.register(Adultpackage)
admin.site.register(Childpackage)
admin.site.register(Review)
admin.site.register(Payments)
admin.site.register(Placed_Booking)
# admin.site.register(BookingLimit)
@admin.register(BookingLimit)
class BookingLimitModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    list_display = ['id', 'max_bookings']
    list_editable = ['max_bookings']

@admin.register(foodCategory)
class foodCategoryModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
@admin.register(fooditem)
class fooditemModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

# @admin.register(BookingFoodOption)
# class BookingFoodOptionModelAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request, obj=None):
#         return False
#     def has_change_permission(self, request, obj=None):
#         return False
#     def has_delete_permission(self, request, obj=None):
#         return False
admin.site.register(BookingFoodOption)


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_editable = ['title',]
    # def has_add_permission(self, request, obj=None):
    #     return False
    # def has_change_permission(self, request, obj=None):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False

@admin.register(item)
class itemModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'item']
    list_editable = ['item']
    # def has_add_permission(self, request, obj=None):
    #     return False
    # def has_change_permission(self, request, obj=None):
    #     return False
    # def has_delete_permission(self, request, obj=None):
    #     return False
def export_reg(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="predict.csv"'
    writer = csv.writer(response)
    writer.writerow(['season','count_adult','count_child','offers'])
    registration = queryset.values_list('season','count_adult','count_child','offers')
    for i in registration:
        writer.writerow(i)
    return response

export_reg.short_description = 'Export to csv'

class predictAdmin(admin.ModelAdmin):
    list_display = ['season','count_adult','count_child','offers']
    actions = [export_reg]
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(predict,predictAdmin)



def export_reg(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registration.csv"'
    writer = csv.writer(response)
    writer.writerow(['User Name','Email','Phone'])
    registration = queryset.values_list('username','email','phone')
    for i in registration:
        writer.writerow(i)
    return response


export_reg.short_description = 'Export to csv'


class RegAdmin(admin.ModelAdmin):
    list_display = ['username','email','phone']
    actions = [export_reg]
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(Account,RegAdmin)



class foodAdmin(admin.ModelAdmin):
    list_display=['username']
    exclude=('password',)
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    verbose_name_plural = "Volunteers Details"
admin.site.register(food_registration,foodAdmin)

class foodcourtLoginAdmin(admin.ModelAdmin):
    list_display=['user']
    exclude=('password',)
    def has_add_permission(self, request, obj=None):
        return False
    # def has_change_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False
    verbose_name_plural = "Food Login Details"
admin.site.register(food_login,foodcourtLoginAdmin)

from django.contrib import admin
from .models import Offer

class OfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percentage','count_adult','count_child', 'active')

admin.site.register(Offer, OfferAdmin)

