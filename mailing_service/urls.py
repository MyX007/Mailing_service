from django.urls import path
from django.views.decorators.cache import cache_page

from mailing_service.services import NewslettersService
from mailing_service.apps import MailingServiceConfig
from mailing_service.views import (NewsletterListView, NewsletterCreateView,
                                   NewsletterDetailView, NewsletterUpdateView,
                                   NewsletterDeleteView, ClientListView,
                                   ClientDetailView, ClientCreateView,
                                   ClientUpdateView, ClientDeleteView,
                                   MessageListView, MessageDetailView,
                                   MessageCreateView, MessageUpdateView,
                                   MessageDeleteView, home_view, Statistic)

app_name = MailingServiceConfig.name

urlpatterns = [
    path(
        'home',
        home_view,
        name='home'
    ),
    path(
        '',
        cache_page(10)(NewsletterListView.as_view()),
        name='newsletters'
    ),
    path(
        'create/',
        cache_page(10)(NewsletterCreateView.as_view()),
        name='create'
    ),
    path(
        'newsletter/<int:pk>/',
        cache_page(10)(NewsletterDetailView.as_view()),
        name='newsletter'
    ),
    path(
        'update/<int:pk>/',
        cache_page(10)(NewsletterUpdateView.as_view()),
        name='update'
    ),
    path(
        'delete/<int:pk>/',
        cache_page(10)(NewsletterDeleteView.as_view()),
        name='delete'
    ),
    path(
        'clients/',
        cache_page(10)(ClientListView.as_view()),
        name='clients'
    ),
    path(
        'client/<int:pk>/',
        cache_page(10)(ClientDetailView.as_view()),
        name='client'
    ),
    path(
        'client/create/',
        cache_page(10)(ClientCreateView.as_view()),
        name='create_client'
    ),
    path(
        'client/update/<int:pk>/',
        cache_page(10)(ClientUpdateView.as_view()),
        name='update_client'
    ),
    path(
        'client/delete/<int:pk>/',
        cache_page(10)(ClientDeleteView.as_view()),
        name='delete_client'
    ),
    path(
        'messages/', cache_page(10)(MessageListView.as_view()),
        name='messages'
    ),
    path(
        'message/<int:pk>/',
        cache_page(10)(MessageDetailView.as_view()),
        name='message'
    ),
    path(
        'message/create/',
        cache_page(10)(MessageCreateView.as_view()),
        name='create_message'
    ),
    path(
        'message/update/<int:pk>/',
        cache_page(10)(MessageUpdateView.as_view()),
        name='update_message'
    ),
    path(
        'message/delete/<int:pk>/',
        cache_page(10)(MessageDeleteView.as_view()),
        name='delete_message'
    ),
    path(
        'start_newsletter/<int:pk>/',
        NewslettersService.start_newsletter,
        name='start_newsletter'
    ),
    path(
        'statistic/',
        cache_page(10)(Statistic.as_view()),
        name='statistic'
    ),
]
