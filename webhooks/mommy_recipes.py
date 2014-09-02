from django.contrib.auth.models import User

from model_mommy.recipe import Recipe

from .models import WebHook

user = Recipe(User)

web_hook = Recipe(WebHook)