from rest_framework import serializers
from .models import Account, Phone, Specs,Voucher
from django.utils import timezone
from datetime import timedelta
from .services import PhoneValidationService
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):

    total_phones = serializers.IntegerField(read_only=True)
    total_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    new_phones_count = serializers.IntegerField(read_only=True)
    discounted_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'user', 'number', 'image',
        'created_at', 'updated_at', 'is_verified', 
        'total_phones', 'total_value', 'new_phones_count', 'discounted_total']

        read_only_fields = ['user', 'created_at', 'updated_at', 'is_verified']


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:

        model = Phone
        fields = ['id', 'account', 'holder', 'name_store', 'type_phone',
        'phone_status', 'amount', 'created_at']
        read_only_fields = ['account', 'created_at']
    
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













