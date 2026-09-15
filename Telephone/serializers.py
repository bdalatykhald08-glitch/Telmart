from rest_framework import serializers
from .models import Account, Phone, Specs,Voucher
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):

    total_phones = serializers.IntegerField(read_only=True)
    total_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    new_phones_count = serializers.IntegerField(read_only=True)
    discounted_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'user', 'number',
        'created_at', 'updated_at', 'is_verified', 
        'total_phones', 'total_value', 'new_phones_count', 'discounted_total']

        read_only_fields = ['user', 'created_at', 'updated_at', 'is_verified']


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:

        model = Phone
        fields = ['id', 'account', 'holder', 'name_store', 'type_phone',
        'phone_status', 'amount', 'created_at', 'add_time']
        read_only_fields = ['account', 'created_at', 'add_time']

    def validate(self, attrs):

        holder = attrs.get('holder')
        name_store = attrs.get('name_store')

        if holder == 'store' and not name_store:
            raise serializers.ValidationError("عندما يكون الأختيار محل يجب عليك وضع أسمه")


        request = self.context.get('request')

        account = request.user.account if request else None
        if request and request.user.is_authenticated:
            account  = getattr(request.user, 'account', None)
            if account:
                add_devices_count = Phone.objects.filter(
                   account=account,
                   add_time__gt=timezone.now()
                ).count()

            if holder == 'person' and add_devices_count >= 1:
               raise serializers.ValidationError("مسموح بأضافة جهاز واحد للشحص خلال اليوم يمكنك الأضافة غدا")

            elif holder == 'store' and add_devices_count >= 10: 
               raise serializers.ValidationError("مسموح بأضافة 10 أجهزة للمحل خلال اليوم يمكنك الأضافة غدا")
        
        return attrs

    #المحاولة تعود بعد يوم 24 ساعة شرط شامل لهما
class SpecsSerializer(serializers.ModelSerializer):

    class Meta:

        model = Specs
        fields = ['id', 'phone', 'processor', 'memory', 'ram', 'battery', 'camera']
      



class VoucherSerializer(serializers.ModelSerializer):

    class Meta:

        model = Voucher
        fields = ['id', 'specs', 'date', 'buyer', 'seller', 'buyer_confirmed', 'seller_confirmed',
        'contract', 'number_IMEI', 'payment_url', 'transfer_id', 'payment_status', 'pdf']

        read_only_fields = ['date', 'buyer', 'seller', 'buyer_confirmed', 'seller_confirmed', 'contract']













