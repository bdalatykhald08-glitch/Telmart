from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
import time
import logging


from .models import Account


@shared_task
def send_welcome_email(account_id):
    time.sleep(3)

    try:

       acccount = Account.objects.get(id=account_id)
       acccount.is_verified = True
       acccount.save()
       
       print(f"{acccount.number}: تم توثيق الحساب بنجاح")
       return True

    except Account.DoesNotExist:
        print(f"رقم الحساب {account_id} غير موجود!")
        return False

logger = logging.getLogger(__name__)

@shared_task
def process_voucher_status(voucher_id, payment_status):

    from .models import Voucher

    try:
        voucher = Voucher.objects.get(id=voucher_id)

        voucher.payment_status = payment_status
        voucher.save()

        logger.info(f"Voucher {voucher_id} updated to status: {payment_status}")
        return f"Voucher {voucher_id} updated successfully"

    except Voucher.DoesNotExist:
        logger.error(f"Voucher with ID {voucher_id} was not found.")
        return False
 


    
    