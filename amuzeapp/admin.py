import csv
from os import path
from django.contrib import admin
from django.http import HttpResponse
from.models import *
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError


admin.site.unregister(Group)
class AdultpackageModelAdmin(admin.ModelAdmin):
    list_display = ['p1_id', 'name', 'price', 'available']
admin.site.register(Adultpackage, AdultpackageModelAdmin)

class ChildpackageModelAdmin(admin.ModelAdmin):
    list_display = ['p2_id', 'name', 'price', 'available']
admin.site.register(Childpackage,ChildpackageModelAdmin)

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

@admin.register(BookingFoodOption)
class BookingFoodOptionModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
# admin.site.register(BookingFoodOption)


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

class BookAdmin(admin.ModelAdmin):
    list_display=['user','p1_id','p2_id','date','count_adult','count_child','total_price','food','paid']
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    verbose_name_plural = "Volunteers Details"
admin.site.register(Placed_Booking,BookAdmin)
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

class paymentAdmin(admin.ModelAdmin):
    list_display=['user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(Payments,paymentAdmin)

from django.contrib import admin
from .models import review
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'review_text', 'rating', 'sentiment')

    def sentiment(self, obj):
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(obj.review_text)
        sentiment_score = scores['compound']
        if sentiment_score >= 0.05:
            return 'Positive'
        elif sentiment_score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    sentiment.short_description = 'Sentiment Analysis'

admin.site.register(review, ReviewAdmin)
