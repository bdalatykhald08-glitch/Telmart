from django.db import IntegrityError, transaction
from Telephone.factory import *
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Make Fake Data For DataBase....."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Continue Make Data ......."))

        

# account one to one 
        users_instance = [UserFactory.build() for _ in range(10000)]
        users = User.objects.bulk_create(users_instance, batch_size=1000)


        account_create = [AccountFactory.build(user=user)  for user in users]
        accounts = Account.objects.bulk_create(account_create, batch_size=1000)     

 
# phone foregn key
        phone_create = [PhoneFactory.build(account=random.choice(accounts))for _ in range(10000)]
        phones = Phone.objects.bulk_create(phone_create, batch_size=1000)


# specs foregn key
        specs_create = [SpecsFactory.build(phone=random.choice(phones))for _ in range(10000)]
        specses = Specs.objects.bulk_create(specs_create, batch_size=1000)


# voucher foregn key
        voucher_create = [VoucherFactory.build
                        (specs=random.choice(specses),
                        buyer=random.choice(users),
                        seller=random.choice(users))for _ in range(10000)]
        
        vouchers = Voucher.objects.bulk_create(voucher_create, batch_size=1000)

            
        self.stdout.write(self.style.SUCCESS("Complete the process Successfully! Completed Full it up DataBase"))


    


    