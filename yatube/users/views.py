from django.views.generic import CreateView
from django.urls import reverse_lazy
from .form import CreationForm

# Проверка авторизованности пользователя
# from ..posts.utils import user_only

class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"
