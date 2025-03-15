from django.core.management.base import BaseCommand
import smtplib
from django.core.mail import send_mail
from django.utils import timezone
from config.settings import EMAIL_HOST_USER
from mailing_service.models import MailingAttempt, Newsletter, Message, Client


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        message_subject = input("Введите тему сообщения: ")
        message_body = input("Введите сообщение: ")
        message = Message.objects.create(
                subject=message_subject,
                body=message_body
        )
        newsletter = Newsletter.objects.create(message=message)
        newsletter.start_datetime = timezone.now()
        newsletter.status = 'Запущена'
        newsletter.save()
        clients = Client.objects.all()

        try:
            response = send_mail(
                subject=message_subject,
                message=message_body,
                from_email=EMAIL_HOST_USER,
                recipient_list=clients,
                fail_silently=False
            )
        except smtplib.SMTPException as e:
            attempt = MailingAttempt(
                status='Ошибка',
                response_mail_service=e,
                newsletter=newsletter,
                datetime=timezone.now()
            )
            attempt.save()

        else:

            attempt = MailingAttempt(
                status='Успешно',
                response_mail_service=response,
                newsletter=newsletter,
                datetime=timezone.now()
            )
            attempt.save()

        finally:
            newsletter.status = 'Завершена'
            newsletter.end_datetime = timezone.now()
            newsletter.save()

        self.stdout.write(self.style.SUCCESS(f"Отправлено: {message_subject}"))
