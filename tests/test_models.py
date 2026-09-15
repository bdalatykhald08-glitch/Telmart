from rest_framework.test import APITestCase
from Telephone.factory import *
from django.contrib.auth import get_user_model

User = get_user_model()


class TestAccountModdel(APITestCase):
    def test_account(self):
        
        expected_data = {
            'number': "9980054320",
            'image': "example_u6778.dat",
            'is_verified': 'True',
        }

        account = AccountFactory(**expected_data)
        for field, value in expected_data.items():

            self.assertEqual(str(getattr(account, field)), value)


    
class TestPhoneModel(APITestCase):
    def test_all_phones_create(self):

        expected_data = {
            'holder': 'person',
            'name_store': 'GlyPHon',
            'type_phone': 'Samsung s21',
            'phone_status': 'used',
            'amount': '2800.0'
        }
  
        phone = PhoneFactory(**expected_data)
        for field, value in expected_data.items():
             
            self.assertEqual(str(getattr(phone, field)), value)


class TestSpecsModel(APITestCase):
    def test_specs_create(self):

        expected_data = {
           'processor': 'snapdragon 8tk',
           'memory': '512GB',
           'ram': '8GB',
           'battery': '5000Ah',
           'camera': '15 Pixel',
        }

        specs = SpecsFactory(**expected_data)
        for field, value in expected_data.items():
            self.assertEqual(str(getattr(specs, field)), value)


class TestVoucherModel(APITestCase):
    def test_voucher_create(self):

        expected_data  = {
           'number_IMEI': '120009384574687',
           'payment_url': 'https://krita.org/en/post-download/',
           'transfer_id': '23111',
           'payment_status': 'PENDING',
        }

        voucher = VoucherFactory(**expected_data)
        for field, value in expected_data.items():
            self.assertEqual(str(getattr(voucher, field)), value)







