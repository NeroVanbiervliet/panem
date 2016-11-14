from django.contrib import admin

# Register your models here.
from .models import Bakery,Product,HasProduct,Category,Logging,Account,Order,Product_order,Token,AdyenPayment,PointPayment,Ingredient,DisableDates, CreditTopUp, PromoCode



admin.site.register(Bakery)
admin.site.register(Product)
admin.site.register(HasProduct)
admin.site.register(Category)
admin.site.register(Logging)
admin.site.register(Account)
admin.site.register(Order)
admin.site.register(Product_order)
admin.site.register(Token)
admin.site.register(AdyenPayment)
admin.site.register(PointPayment)
admin.site.register(Ingredient)
admin.site.register(DisableDates)
admin.site.register(CreditTopUp)
admin.site.register(PromoCode)
