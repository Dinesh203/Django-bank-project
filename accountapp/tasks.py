
from celery import shared_task
from django.conf import settings
from BankingSystem import settings
from django.core.mail import send_mail
# from celery.utils.log import get_task_logger
# from time import sleep
from time import time


# logger = get_task_logger(__name__)

@shared_task
def send_mail_task():
    print("send mail ready")
    subject = 'Celery Implementation'
    email_body = "this is email body celery mail schedule done"
    recipient = ['dinesh.parihar@cubexo.io', ]
    send_mail(subject, email_body, settings.EMAIL_HOST_USER, recipient)
    return "Mail has been sent........"




# @task(name='my_first_task')
# def my_first_task_hello(duration):
#     sleep(duration)
#     return ('first_task_done')
#
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# @periodic_task(
# run_every=(crontab(hour=3, minute=34)), #runs exactly at 3:34am every day
# name="Dispatch_scheduled_mail",
# reject_on_worker_lost=True,
# ignore_result=True)
# def schedule_mail():
#     message = render_to_string('app/schedule_mail.html')
#     mail_subject = 'Scheduled Email'
#     to_email = getmail
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     email.send()
