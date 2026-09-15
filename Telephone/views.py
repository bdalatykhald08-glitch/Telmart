from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Account, Phone, Specs, Voucher
from .serializers import AccountSerializer, PhoneSerializer, SpecsSerializer, VoucherSerializer
from django.db.models import Count, Sum, F, Q, ExpressionWrapper, DecimalField
from decimal import Decimal
from .tasks import send_welcome_email, process_voucher_status
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

User = get_user_model()


# Create your views here.


def mobile_view(request):
    return render(request, 'mobile.html')


class AccountViewSet(viewsets.ModelViewSet):

    queryset = Account.objects.select_related('user').annotate(
        total_phones=Count('phones'),
        total_value=Sum('phones__amount'),
        new_phones_count=Count('phones', filter=Q(phones__phone_status='new')),
        discounted_total=Sum(
            ExpressionWrapper(
               F('phones__amount') * Decimal('0.8'),
               output_field=DecimalField())
        )
    ).order_by('id')
     
    serializer_class = AccountSerializer
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['number']


    # clean function for save user
    def perform_create(self, serializer):
        account = serializer.save(user=self.request.user)

        send_welcome_email.delay(account.id)
      

        @method_decorator(cache_page(60))
        def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)
   
        
class PhoneViewSet(viewsets.ModelViewSet):

    queryset = Phone.objects.select_related('account').order_by('id')
    serializer_class = PhoneSerializer
    #permission_classes = [IsAuthenticated] 
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type_phone', 'amount']

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)

class SpecsViewSet(viewsets.ModelViewSet):

    queryset = Specs.objects.select_related('phone').order_by('id')
    serializer_class = SpecsSerializer
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['memory']
    search_fields = ['ram']
    

class VoucherViewSet(viewsets.ModelViewSet):

    queryset = Voucher.objects.select_related('specs', 'buyer', 'seller').order_by('id')
    serializer_class = VoucherSerializer
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['number_IMEI']


    def perform_create(self, serializer):
        specs = serializer.validated_data.get('specs')


        if not specs:
            raise serializers.ValidationError({"specs": "هذا الحقل مطلوب"})
        seller_user = specs.phone.account.user
        buyer_user = self.request.user

        voucher = serializer.save(buyer=buyer_user, seller=seller_user)
        payment_status = voucher.payment_status
             
        delay_seconds = 10 if payment_status in ['PENDING', 'PAID_HELD', 'REFUNDED'] else 5

        process_voucher_status.apply_async(
            args=[voucher.id, payment_status],
            countdown=delay_seconds
        )

