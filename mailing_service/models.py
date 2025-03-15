from django.db import models
from users.models import User

# Create your models here.

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Имя"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )
    comment = models.TextField(
        max_length=150,
        verbose_name="Комментарий"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        **NULLABLE
    )

    def __str__(self):
        return f'{self.email} ({self.name})'

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    subject = models.CharField(
        max_length=255,
        verbose_name="Тема сообщения"
    )
    body = models.TextField(
        max_length=255,
        verbose_name="Сообщение"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        **NULLABLE)

    def __str__(self):
        return f'{self.subject}: {self.body}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Newsletter(models.Model):
    start_datetime = models.DateTimeField(
        verbose_name="Начало отправки",
        **NULLABLE
    )
    end_datetime = models.DateTimeField(
        verbose_name="Конец отправки",
        **NULLABLE
    )
    status = models.CharField(
        max_length=50,
        verbose_name="Статус отправки"
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        related_name="newsletter"
    )
    clients = models.ManyToManyField(Client, verbose_name="Получатели")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        **NULLABLE
    )

    def __str__(self):
        return f"{Message.body} ({self.start_datetime} - {self.end_datetime})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ['message', 'author']
        permissions = [('can_stop_newsletter', 'Can stop newsletter')]


class MailingAttempt(models.Model):
    datetime = models.DateTimeField(
        verbose_name="Дата и время попытки"
    )
    status = models.CharField(
        max_length=50,
        verbose_name="Статус"
    )
    response_mail_service = models.CharField(
        max_length=50,
        verbose_name="Ответ почтового сервера"
    )
    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE,
        verbose_name="Рассылка",
        related_name='attempt'
    )

    def __str__(self):
        return f"{self.datetime} ({self.newsletter})"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
