from django.db import models, transaction
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta



# Create your models here.


class Account(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    number = models.CharField(max_length=10, unique=True, validators=[RegexValidator(r'^\d{10}', 'أدخل رقم الجوال بدون المفتاح ')])
    image = models.ImageField(upload_to='image/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):

        user_obj = getattr(self, 'user', None)
        return user_obj.username  if user_obj else f"Account {self.number}"

    
    class Meta:

        ordering = ['-created_at']
        


# function timezone for class Phone 
def one_day_hence():
    return timezone.now() + timedelta(days=1)

class Phone(models.Model):

    PHONE_STATUS = [
        ('new', 'جديد'), ('used', 'مستعمل')
    ]

    HOLDER_CHOICE = [
        ('store', 'محل'), ('person', 'شخص')
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='phones')
    holder = models.CharField(max_length=50, choices=HOLDER_CHOICE)
    name_store = models.CharField(max_length=50, blank=True, null=True, help_text='للمحل يجب وضع أسمه')
    type_phone = models.CharField(max_length=50, help_text='smasung s22 نوع الجهاز باسمه مثل')
    phone_status = models.CharField(max_length=50, choices=PHONE_STATUS, help_text='حالة الجهاز')
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text='المبلغ بالجنيه السوداني')
    created_at = models.DateTimeField(auto_now_add=True)
    add_time = models.DateTimeField(default=one_day_hence)

    def __str__(self):

        return self.type_phone

    @property
    def is_add_limit(self):
        return timezone.now() < self.add_time
    
    class Meta:

        ordering = ['-created_at']


class Specs(models.Model):


    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name='specss')
    processor = models.CharField(max_length=50, verbose_name='المعالج')
    memory = models.CharField(max_length=50, verbose_name='ذاكرة')
    ram = models.CharField(max_length=50, verbose_name='رام')
    battery = models.CharField(max_length=50, verbose_name='البطارية')
    camera = models.CharField(max_length=50, verbose_name='كاميرا')

    
    def __str__(self):

        phone_obj = getattr(self, 'phone')
        if phone_obj:
            return f"{phone_obj.type_phone} - {self.processor}"
        
        return f"Specs - {self.processor}"
        
    class Meta:

        ordering = ['-id']


class Voucher(models.Model):

    PAYMENT_STATUS = [
       ('PENDING', 'في انتظار الدفع'),
       ('PAID_HELD', 'تم الدفع ومحجوز لدي المنصة'),
       ('COMPLETED', 'مكتمل وتم التسليم'),
       ('REFUNDED', 'تم أرجاع المال للمشتري'),
       ('FAILED', 'فشلت العملية'),
    ]
    
    specs = models.ForeignKey(Specs, on_delete=models.CASCADE, related_name='vouchers')
    date = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='buyers')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sellers')
    number_IMEI = models.CharField(max_length=15, unique=True, validators=[RegexValidator(r'^\d{15}$', 'الأرقام الصحيحة تتكون من 15 رقم')])
    buyer_confirmed = models.BooleanField(default=False)
    seller_confirmed = models.BooleanField(default=False)
    contract = models.BooleanField(default=False)
    payment_url = models.URLField(blank=True, null=True, help_text='طريقة الدفع عن طريق محفظة ألكترونية مثل ماي كاشي')
    transfer_id = models.CharField(max_length=25, blank=True, null=True, help_text='أرقام العملية لتحويلة ')
    payment_status = models.CharField(max_length=45, choices=PAYMENT_STATUS, default='PENDING')
    pdf = models.FileField(help_text='PDF الحصول علي ألايصال بصيغة', null=True, blank=True)


    def __str__(self):
        return self.number_IMEI

    class Meta:

        ordering = ['-date']

    @transaction.atomic
    def confirm_and_release(self):

        if self.payment_status != 'PAID_HELD':
            raise ValidationError("لايمكن تحرير المبلغ قبل أتمام الدفغ وحجزه لدي المنصة")

        if not (self.buyer_confirmed and self.seller_confirmed):
            raise ValidationError("IMEI يجب موافقة الطرفين ومطابقة رقم")

        self.payment_status = 'COMPELTED'
        self.contract =True

        self.save()


    @property
    def type_phone(self):
        return self.specs.phone.type_phone


    @property
    def amount(self):
        return self.specs.phone.amount





