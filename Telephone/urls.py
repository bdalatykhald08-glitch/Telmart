
from .views import AccountViewSet, PhoneViewSet, SpecsViewSet, VoucherViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import mobile_view


router = DefaultRouter()

router.register(r'accounts', AccountViewSet,  basename='account'),
router.register(r'phones', PhoneViewSet, basename='phone'),
router.register(r'specses', SpecsViewSet, basename='specs'),
router.register(r'vouchers', VoucherViewSet, basename='voucher'),


urlpatterns = [
    # html page
    path('', include(router.urls)),
    path('mobile', mobile_view, name='mobile'),
]



