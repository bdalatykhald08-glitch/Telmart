from django.db.models.signals import post_save 
from django.dispatch import receiver
from django.conf import settings 
from .models import Account

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_account(sender, instance, created, **kwargs):

   if created:    
        Account.objects.get_or_create(user=instance)

# لغيتها عشان ما تعمل مستخدم عشوائى بنفس رقم المعرفي 2 
# وعملها عندما يكون منتج بعد الغاء الأعتماد علي Factory


