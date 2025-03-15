from users.models import User
from django.shortcuts import redirect
from django.urls import reverse


class BlockUser:

    @staticmethod
    def block(request, pk):
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()

        return redirect(reverse("users:profile", kwargs={"pk": pk}))

    @staticmethod
    def unblock(request, pk):
        user = User.objects.get(pk=pk)
        user.is_active = True
        user.save()

        return redirect(reverse("users:profile", kwargs={"pk": pk}))
