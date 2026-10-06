from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Account, Phone, Specs, Voucher
from .serializers import AccountSerializer, PhoneSerializer, SpecsSerializer, VoucherSerializer
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

User = get_user_model()

 
# Create your views here.


def mobile_view(request):
    return render(request, 'mobile.html')


class AccountViewSet(viewsets.ModelViewSet):
     
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['number']


    # clean function for save user
    def get_queryset(self):
        return Account.objects.with_financial_annotations()
    
    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)

        @method_decorator(cache_page(60))
        def list(self, request, *args, **kwargs):
            return super().list(request, *args, **kwargs)
   
        
class PhoneViewSet(viewsets.ModelViewSet):

    queryset = Phone.objects.select_related('account').order_by('id')
    serializer_class = PhoneSerializer
    permission_classes = [IsAuthenticated] 
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type_phone', 'amount']

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)


class SpecsViewSet(viewsets.ModelViewSet):

    queryset = Specs.objects.select_related('phone').order_by('id')
    serializer_class = SpecsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['memory']
    search_fields = ['ram']

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)


class VoucherViewSet(viewsets.ModelViewSet):

    queryset = Voucher.objects.select_related('specs', 'buyer', 'seller').order_by('id')
    serializer_class = VoucherSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['number_IMEI']

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)


