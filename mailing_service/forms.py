from django import forms
from django.forms import BooleanField

from mailing_service.models import Newsletter, Client, Message


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check'
            else:
                field.widget.attrs['class'] = 'form-control'


class NewsletterForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('message', 'clients')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(NewsletterForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['message'].queryset = Message.objects.filter(
                author=user
            )
            self.fields['clients'].queryset = Client.objects.filter(
                author=user
            )


class ClientForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'comment')


class MessageForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'body')
