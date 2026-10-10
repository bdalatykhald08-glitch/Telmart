from rest_framework import serializers
from .models import Account, Phone, Specs,Voucher
from django.contrib.auth import get_user_model
from django.db import transaction
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    number = serializers.CharField(max_length=10, required=False, allow_null=True,  allow_blank=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'number', 'image']

    def create(self, validated_data):
        number = validated_data.pop('number', None)
        image = validated_data.pop('image', None)

        is_verified = bool(number and image)

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)

            Account.objects.update_or_create(user=user, number=number, image=image, is_verified=is_verified)

        return user
    
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


class SpecsSerializer(serializers.ModelSerializer):

    class Meta:

        model = Specs
        fields = ['id', 'processor', 'memory', 'ram', 'battery', 'camera']

      
class PhoneSerializer(serializers.ModelSerializer):

    phone_specs = SpecsSerializer()

    class Meta:

        model = Phone
        fields = ['id', 'account', 'holder', 'name_store', 'type_phone',
        'phone_status', 'amount', 'phone_specs', 'image_phone', 'created_at']
        read_only_fields = ['account', 'created_at']

    def create(self, validated_data):
        specs_data = validated_data.pop('phone_specs')

        phone = Phone.objects.create(**validated_data)

        Specs.objects.create(phone_specs=phone, **specs_data)

        return phone
    
    #المحاولة تعود بعد يوم 24 ساعة شرط شامل لهما

class VoucherSerializer(serializers.ModelSerializer):
    phone_details = PhoneSerializer(source='phone_voucher', read_only=True)
    class Meta:

        model = Voucher
        fields = ['id', 'phone_voucher', 'date', 'buyer', 'seller', 'buyer_confirmed', 'seller_confirmed',
        'contract', 'number_IMEI', 'phone_details', 'payment_url', 'transfer_id', 'payment_status', 'pdf']

        read_only_fields = ['date', 'buyer', 'seller', 
                            'buyer_confirmed', 'seller_confirmed', 'payment_status', 'contract']













