import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from Telephone.factory import *
import uuid
User = get_user_model()


@pytest.fixture
def api():
    return APIClient()

@pytest.fixture
def unique_user(db):
    unique_username = f"user_{uuid.uuid4().hex[:8]}"
    return User.objects.create_user(
        username=unique_username,
        email=f"{unique_username}@test.com",
        password="password123"
    )

@pytest.fixture
def sample_account(db, unique_user):
    return AccountFactory(user=unique_user) # duplicate

@pytest.fixture
def sample_phone(db, sample_account):
    return PhoneFactory(account=sample_account)


@pytest.fixture
def sample_specs(db, sample_phone):
    return SpecsFactory(phone=sample_phone)


@pytest.fixture
def sample_voucher(db, sample_specs, unique_user):

    return VoucherFactory(
        specs=sample_specs,
        buyer=unique_user,
        seller=unique_user,
        buyer_confirmed=False,
        seller_confirmed=False
    )


