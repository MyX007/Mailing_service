from django.contrib import admin

from mailing_service.models import Client, Message, Newsletter


# Register your models here.


@admin.register(Client)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "comment")
    search_fields = ("name",)
    ordering = ("email",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
    search_fields = ("subject",)
    ordering = ("subject",)


@admin.register(Newsletter)
class MailshotAdmin(admin.ModelAdmin):
    list_display = ("message",)
    list_filter = ("status",)
    search_field = ("message",)
