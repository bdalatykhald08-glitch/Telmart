from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Account, Phone,  Voucher
from .serializers import AccountSerializer, PhoneSerializer,  VoucherSerializer, RegisterSerializer
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import CreateAPIView
from django.core.exceptions import ValidationError
from django.db.models import  Q
User = get_user_model()

 
# Create your views here.


def mobile_view(request):
    return render(request, 'mobile.html')

class RegisterViewSet(CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
class AccountViewSet(viewsets.ReadOnlyModelViewSet):
     
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    # clean function for save user
    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).with_financial_annotations()
    

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
   
        
class PhoneViewSet(viewsets.ModelViewSet):

    queryset = Phone.objects.select_related('account')
    serializer_class = PhoneSerializer
    permission_classes = [IsAuthenticated] 
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type_phone', 'amount', 'phone_status', 'holder']
    search_fields = ['type_phone', 'name_store']

    
    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)



class VoucherViewSet(viewsets.ModelViewSet):

    serializer_class = VoucherSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['number_IMEI']


    def get_queryset(self):
        return Voucher.objects.select_related('phone_voucher__account', 'buyer', 'seller').filter(
            Q(buyer=self.request.user) | Q(seller=self.request.user)
        )

    
    def perform_create(self, serializer):
        buyer = self.request.user
        phone = serializer.validated_data['phone_voucher']
        seller = phone.account.user

        if buyer  == seller:
            raise ValidationError("لايمكن أن يكون البائع والمشتري نفس الشخص")

        serializer.save(
            buyer=buyer,
            seller=seller,
            payment_status='PENDING'
        )


        