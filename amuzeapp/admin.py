import csv
from django.contrib import admin
from django.http import HttpResponse
from.models import *
from django.contrib.auth.models import Group
# Register your models here.

admin.site.unregister(Group)
admin.site.register(fooditem)
admin.site.register(foodCategory)
admin.site.register(Adultpackage)
admin.site.register(Childpackage)
admin.site.register(Reviews)
admin.site.register(Payments)
admin.site.register(Placed_Booking)


 
# admin.site.register(Category)
# class food_loginModelAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request, obj=None):
#         return False
#     def has_change_permission(self, request, obj=None):
#         return False
#     def has_delete_permission(self, request, obj=None):
#         return False
# admin.site.register(food_login)


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