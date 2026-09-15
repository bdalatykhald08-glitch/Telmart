from rest_framework.test import APITestCase
from rest_framework import status
from Telephone.factory import *
from Telephone.models import *
from django.test import override_settings
from django.contrib.auth import get_user_model

User = get_user_model()


class TestRemainingViews(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.account = AccountFactory(user=self.user)
        self.phone = PhoneFactory(account=self.account)
        self.specs = SpecsFactory(phone=self.phone)
        self.voucher = VoucherFactory(specs=self.specs)

        self.client.force_authenticate(user=self.user)

    def test_get_endpoints_status_ok(self):
        endpoints = [
            ('/accounts/'),
            ('/phones/'),
            ('/specses/'),
            ('/vouchers/')
        ]

        for url in endpoints:
            with self.subTest(url=url):
                request = self.client.get(url)
            
                self.assertEqual(request.status_code, status.HTTP_200_OK)
              
    
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def  test_account_runs_celery_task(self):
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
            
        payload = {
            'number': '0987887659',
            'image': "example_u6778.dat",
            'is_verified': False
            }
        response = self.client.post('/accounts/', payload)
        print("Account Error Response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    

    def test_create_phone_view_success(self):
        new_user = UserFactory()
        AccountFactory(user=new_user)
        self.client.force_authenticate(user=new_user)

        payload = {
            'holder': 'person',
            'name_store': 'GlyPhon',
            'type_phone': 'Samsung s21',
            'phone_status': 'used',
            'amount': '2800.0'
        }

        response = self.client.post('/phones/', payload)
        print("Phone Error Response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_specs_view_success(self):
        new_user = UserFactory()
        new_account = AccountFactory(user=new_user)
        new_phone = PhoneFactory(account=new_account)
        self.client.force_authenticate(user=new_user)
        payload = {
            'phone': new_phone.id,
            'processor': 'Snapdragon 8 gen 4',
            'memory': '512GB',
            'ram': '8GB',
            'battery': '5000Ah',
            'camera': '5 Pixel'
        }

        
        response = self.client.post('/specses/', payload)
        print("Specs Error Response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_voucher_view_success(self):
        new_user = UserFactory()
        new_account = AccountFactory(user=new_user)
        new_phone = PhoneFactory(account=new_account)
        new_specs = SpecsFactory(phone=new_phone)

        self.client.force_authenticate(user=new_user)
        payload = {
            'specs': new_specs.id,
            'number_IMEI': '183759387630091',
            'payment_status': 'PENDING'
        
        }

        response = self.client.post('/vouchers/', payload)
        print("Voucher Error Response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)















    