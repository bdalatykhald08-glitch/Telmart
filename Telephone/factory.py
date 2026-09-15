import factory
from faker import Faker
from .models import *
import random
from django.contrib.auth import get_user_model

User = get_user_model()


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"otay_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")


class AccountFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)
    number = factory.Sequence(lambda n: f"{n+1:010d}")
    image = factory.django.ImageField()
    is_verified = factory.Faker('boolean')

    
class PhoneFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Phone
       
    account = factory.SubFactory(AccountFactory)
    holder = factory.Faker('random_element', elements=['store', 'person'])
    name_store = factory.Faker('random_element', elements=['techPo', 'HamzaPhone', 'KTell', 'phoneStad', 'yesatech', 'markmob'])
    type_phone = factory.Faker('sentence', nb_words=3)
    phone_status = factory.Faker('random_element', elements=['new', 'used'])
    amount = factory.Faker('pydecimal', right_digits=2, left_digits=6, positive=True)


class SpecsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Specs
        
    phone = factory.SubFactory(PhoneFactory)
    processor = factory.LazyFunction(lambda: f"معالج {random.randint(1, 9999)}")
    memory = factory.LazyFunction(lambda: f"{random.choice([32, 64, 128, 256, 512])} جيجا")
    ram = factory.LazyFunction(lambda: f"{random.choice([4, 8, 12, 16, 24])} جيجا")
    battery = factory.LazyFunction(lambda: f"{random.randint(3000, 7000)} ملي ")
    camera = factory.LazyFunction(lambda: f"{random.randint(8, 200)} ميجا") 


class VoucherFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Voucher

    specs = factory.SubFactory(SpecsFactory)
    buyer = factory.SubFactory(UserFactory)
    seller = factory.SubFactory(UserFactory)
    number_IMEI = factory.Sequence(lambda n: f"{n+1:015d}")
    buyer_confirmed = factory.Faker('boolean')
    seller_confirmed = factory.Faker('boolean')
    contract = factory.Faker('boolean')
    payment_url = factory.Faker('url')
    transfer_id = factory.Faker('word')
    payment_status = factory.Faker('random_element',  elements=['PENDING', 'PAID_HELD', 'COMPLETED', 'REFUNDED', 'FAILED'])
    pdf = factory.django.FileField()











