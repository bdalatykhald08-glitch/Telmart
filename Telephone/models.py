from django.db import models, transaction
from django.conf import settings
from django.core.validators import RegexValidator
from django.db.models import Count, Sum, F, Q, ExpressionWrapper, DecimalField, Value
from decimal import Decimal
from django.db.models.functions import Coalesce

# Create your models here.
class AccountQueryset(models.QuerySet):
    def with_financial_annotations(self):
        return self.select_related('user').annotate(
            total_phones=Count('phones'),
            total_value=Coalesce(Sum('phones__amount'), Value(0), output_field=DecimalField()),
            new_phones_count=Count('phones', filter=Q(phones__phone_status='new')),
            discounted_total=Sum(
                ExpressionWrapper(
                   F('phones__amount') * Decimal('0.8'),
                     output_field=DecimalField())
                )
            ).order_by('id')


class Account(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user')
    number = models.CharField(max_length=10, blank=True, null=True, validators=[RegexValidator(r'^\d{10}', 'أدخل رقم الجوال بدون المفتاح ')])
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    objects = AccountQueryset.as_manager()

    def save(self, *args, **kwargs):

        if self.number and self.image:
            self.is_verified = True

        else:
            self.is_verified = False
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.user}"
    
    class Meta:

        ordering = ['-created_at']
        

# function timezone for class Phone 


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


    def __str__(self):

        return self.type_phone
    
    class Meta:

        ordering = ['-created_at']


class Specs(models.Model):


    phone_specs = models.OneToOneField(Phone, on_delete=models.CASCADE, related_name='phone_specs')
    processor = models.CharField(max_length=50, verbose_name='المعالج')
    memory = models.CharField(max_length=50, verbose_name='ذاكرة')
    ram = models.CharField(max_length=50, verbose_name='رام')
    battery = models.CharField(max_length=50, verbose_name='البطارية')
    camera = models.CharField(max_length=50, verbose_name='كاميرا')

    
    def __str__(self):

        return f"{self.phone_specs}"
        
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
    
    phone_voucher = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name='voucher')
    date = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='buyers')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sellers')
    number_IMEI = models.CharField(max_length=15, unique=True, validators=[RegexValidator(r'^\d{15}$', 'الأرقام الصحيحة تتكون من 15 رقم')])
    buyer_confirmed = models.BooleanField(default=False)
    seller_confirmed = models.BooleanField(default=False)
    contract = models.BooleanField(default=True)
    payment_url = models.URLField(blank=True, null=True, help_text='طريقة الدفع عن طريق محفظة ألكترونية مثل ماي كاشي')
    transfer_id = models.CharField(max_length=25, blank=True, null=True, help_text='أرقام العملية لتحويلة ')
    payment_status = models.CharField(max_length=45, choices=PAYMENT_STATUS)
    pdf = models.FileField(help_text='PDF الحصول علي ألايصال بصيغة', null=True, blank=True)


    def __str__(self):
        return self.number_IMEI

    class Meta:

        ordering = ['-date']

    @property
    def type_phone(self):
        return self.phone.type_phone


    @property
    def amount(self):
        return self.phone.amount





