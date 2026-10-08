import logging
from django.db import transaction
from .models import  Voucher
from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)


@shared_task
def process_voucher_status(voucher_id, payment_status):

    with transaction.atomic():
        voucher = Voucher.objects.select_for_update().get(id=voucher_id)
        voucher.payment_status = payment_status
        voucher.save(update_fields=['payment_status'])

        logger.info(f"Voucher {voucher_id} updated to status: {payment_status}")
        return f"Voucher {voucher_id} {payment_status} updated successfully"


    

