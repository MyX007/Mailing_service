import smtplib
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from config.settings import CACHE_ENABLED, EMAIL_HOST_USER
from mailing_service.models import MailingAttempt, Newsletter


class NewslettersService:

    @staticmethod
    def start_newsletter(request, pk):
        newsletter = Newsletter.objects.get(pk=pk)
        subject = newsletter.message.subject
        message = newsletter.message.body
        newsletter.start_datetime = timezone.now()
        newsletter.status = 'Запущена'
        newsletter.save()
        clients = []

        for client in newsletter.clients.all():
            clients.append(client.email)

        try:
            response = send_mail(
                subject=subject,
                message=message,
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
            return redirect(reverse("mailing_service:newsletters"))

    @staticmethod
    def caching(queryset, model, user=None):
        if not CACHE_ENABLED:
            return queryset.filter(author=user)
        key = str(model) + "_list"
        objects = cache.get(key)
        if objects is not None:
            return objects
        objects = queryset.filter(author=user)
        cache.set(key, objects, 60 * 1)
        return objects
