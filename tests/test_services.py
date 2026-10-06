import pytest
from Telephone.services import PhoneValidationService, VoucherEscrowService
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_holder_store_limits(unique_user):

    class MockRequest:
        def __init__(self, user):
            self.user = user

    request = MockRequest(user=unique_user)

    attrs = {'holder': 'store', 'name_store': None}

    with pytest.raises(ValidationError):
       PhoneValidationService.validate_check_limits(attrs, request)
     

# duplicate
@pytest.mark.django_db
def test_voucher_confirmed(sample_voucher):

    sample_voucher.buyer_confirmed = True
    sample_voucher.seller_confirmed = False
    sample_voucher.save()
    value = 10
    with pytest.raises(ValidationError):
        VoucherEscrowService.confirm_and_release(sample_voucher, value)
        











        



