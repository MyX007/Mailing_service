from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  DeleteView, TemplateView)

from mailing_service.forms import NewsletterForm, ClientForm, MessageForm
from mailing_service.models import Client, MailingAttempt, Message, Newsletter


# Create your views here.


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    permission_required = ('mailing_service.add_newsletter')
    success_url = reverse_lazy('mailing_service:newsletters')

    def form_valid(self, form):
        newsletter = form.save()
        user = self.request.user
        newsletter.author = user
        newsletter.status = "Создана"
        newsletter.save()

        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    permission_required = ('mailing_service.change_newsletter')
    success_url = reverse_lazy('mailing_service:newsletter')

    def get_success_url(self):
        return reverse(
            'mailing_service:newsletter',
            kwargs={'pk': self.object.pk}
        )


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('mailing_service:newsletters')
    permission_required = ('mailing_service.delete_newsletter')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    permission_required = ('mailing_service.view_client')


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_service:clients')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.author = user
        client.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = ('mailing_service.change_client')
    success_url = reverse_lazy('mailing_service:client')

    def get_success_url(self):
        return reverse('mailing_service:client', kwargs={'pk': self.object.pk})


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_service:clients')
    permission_required = ('mailing_service.delete_client')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = ('mailing_service.create_message')
    success_url = reverse_lazy('mailing_service:messages')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.author = user
        message.save()

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = ('mailing_service.change_message')
    success_url = reverse_lazy('mailing_service:messages')

    def get_success_url(self):
        return reverse(
            'mailing_service:message',
            kwargs={'pk': self.object.pk}
        )


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_service:messages')
    pemission_required = ('mailing_service.delete_message')


class Statistic(TemplateView):
    template_name = 'mailing_service/statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        newsletters = Newsletter.objects.filter(author=user)
        attempts = MailingAttempt.objects.filter(newsletter__in=newsletters)
        fail_status = 0
        success_status = 0
        newsletters_count = 0

        for attempt in attempts:
            if attempt.status == 'Ошибка':
                fail_status += 1
            elif attempt.status == 'Успешно':
                success_status += 1
                newsletters_count += attempt.newsletter.clients.count()

        context["successful"] = success_status
        context["failed"] = fail_status
        context["newsletters_count"] = newsletters_count
        context["attempts"] = attempts.count()
        return context


def home_view(request):
    newsletters = Newsletter.objects.count()
    started = Newsletter.objects.filter(status='started').count()
    clients = Client.objects.count()
    context = {'newsletters': newsletters,
               'started': started,
               'clients': clients}

    return render(request, 'mailing_service/home.html', context)


