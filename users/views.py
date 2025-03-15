import secrets
import string
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from config import settings
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User


# Create your views here.


class RegisterView(generic.CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке для подтверждения завершения регистрации: {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


def user_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = User


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        return self.request.user


class ProfileListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "users/profile_list.html"


def reset_password(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        if not User.objects.filter(email=email).exists():
            return render(
                request,
                template_name='users/reset_password.html'
            )
        else:
            user = get_object_or_404(User, email=email)
            new_password = ''.join(
                random.choices(
                    string.ascii_letters + string.digits, k=8
                )
            )
            user.set_password(new_password)
            user.save()
            send_mail(
                subject='Сброс пароля',
                message=f'Ваш новый пароль: {new_password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
            )
        return redirect(reverse('users:login'))

    return render(request, template_name='users/reset_password.html')
