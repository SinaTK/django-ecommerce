from celery import shared_task
from accounts.models import OTPcode
from datetime import timedelta, datetime
import pytz

@shared_task
def remove_expired_otpcodes():
    expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
    ex_codes = OTPcode.objects.filter(created__lt=expired_time)
    num = ex_codes.count()
    ex_codes.delete()
    if num:
        message = '{} expired codes was deleted'.format(num)
    else:
        message = 'No expired code was found'
    print(message)