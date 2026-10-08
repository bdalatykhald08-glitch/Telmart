
from .views import AccountViewSet, PhoneViewSet, SpecsViewSet, VoucherViewSet, RegisterViewSet
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
    path('mobile/', mobile_view, name='mobile'),
    path('api/register/', RegisterViewSet.as_view(), name='register'),
    path('', include(router.urls)),
]



