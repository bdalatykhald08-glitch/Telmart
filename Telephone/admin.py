from django.contrib import admin
from .models import *

# Register your models here
class SpecsInline(admin.StackedInline):
    model = Specs
    extra = 1
  


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'number', 'is_verified')
    search_fields = ('user__username', 'number')
    list_filter = ('is_verified',)

    def has_add_permission(self, request):
        return False

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_phone', 'amount', 'phone_status', 'account')
    list_filter = ('phone_status', 'holder')
    search_fields = ('type_phone', 'name_store')
    inlines = [SpecsInline]



@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('id', 'number_IMEI', 'phone_voucher',  'buyer', 'seller', 'payment_status')
    list_filter = ('payment_status',)
    search_fields = ('number_IMEI',)

