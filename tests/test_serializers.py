from  django.test import TestCase
from  Telephone.serializers import *
from  Telephone.factory import *
from django.contrib.auth import get_user_model

User = get_user_model()


class TestSeializersInput(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.account = AccountFactory(user=self.user)
        self.phone = PhoneFactory(account=self.account)
        self.specs = SpecsFactory(phone=self.phone)
        self.voucher = VoucherFactory(specs=self.specs)


    def test_account_serializer_data(self):
        payload = {
          
            'number': "9980054320",
            'image': "example_u6778.dat",
            'is_verified': False,
        }

        
        serializer = AccountSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
     


    def test_phone_serializer_input(self):
        payload = {
           
            'holder': 'person',
            'name_store': 'GlyPhon',
            'type_phone': 'Samsung s21',
            'phone_status': 'used',
            'amount': '2800.0'
        }

        serializer = PhoneSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)



    def test_specs_serializer_input(self):
        payload = {
            'phone': self.phone.id,
            'processor': 'Snapdragon 8 gen 4',
            'memory': '512GB',
            'ram': '8GB',
            'battery': '5000Ah',
            'camera': '5 Pixel'
        }

        serializer = SpecsSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
    


    def test_voucher_serializer_input(self):
        payload = {
            'specs': self.specs.id,
            'number_IMEI': '183759387630091',
            'payment_status': 'PENDING'
             
        }

        serializer = VoucherSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
      
class TestAllSerializersOutput(TestCase):

    def test_serializers_output(self):

        serializers_to_test = [
           (
           PhoneFactory(),
           PhoneSerializer,
           ['holder', 'name_store', 'type_phone',
           'phone_status', 'amount']
           ),

           (
            SpecsFactory(),
            SpecsSerializer,
            ['processor', 'memory', 'ram', 'battery', 'camera']   
           ),

           (
            VoucherFactory(),
            VoucherSerializer,
            ['number_IMEI',  'payment_status']   
           )
            
        ]

        for instance, serializer_class, fields in serializers_to_test:
            serializer_data = serializer_class(instance).data

            for field in fields:
                with self.subTest(serializer=serializer_class.__name__, field=field):
                    self.assertEqual(
                        str(serializer_data[field]),
                        str(getattr(instance, field))
                    )









