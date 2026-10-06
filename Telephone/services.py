from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Phone
from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneValidationService:

    @staticmethod
    def validate_check_limits(attrs, request):
        holder = attrs.get('holder')
        name_store = attrs.get('name_store')
    
        if holder == 'store' and not  name_store:
           raise ValidationError("عندما يكون الأختيار محل يجب عليك وضع أسمه")
        
        elif holder == 'person':
           raise ValidationError("أكتب أسمك")
    
        account = getattr(request.user, 'account', None)
        if account:
            last_24_hours = timezone.now() - timedelta(days=1)
            add_devices_count = Phone.objects.filter(
                account=account,
                created_at__gte=last_24_hours
            ).count()
            limits = {'person': 1, 'store': 10}
            max_allowed = limits.get(holder, 1)

            if add_devices_count >= max_allowed:
                raise ValidationError(f'يمكنك الأضافة خلال 24 ساعة {max_allowed}')
            
        return attrs
    

class VoucherEscrowService:
    @transaction.atomic
    def confirm_and_release(self, value):
        # الشرط  لاحقا عندما أتواصل مع بوابة دفع لعملية حجز المال 

        #if self.payment_status != 'PAID_HELD':
           # raise ValidationError("لايمكن تحرير المبلغ قبل أتمام الدفغ وحجزه لدي المنصة")
    
        if self.buyer_confirmed and self.seller_confirmed == False:
            raise ValidationError(" يجب موافقة الطرفين ")

        else:
    
         #   self.payment_status = 'COMPLETED'
            self.contract = True
            self.save()

        return value
















