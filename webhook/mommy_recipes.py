from django.contrib.auth.models import User

from model_mommy.recipe import Recipe, foreign_key, seq

from .models import WebHook

user = Recipe(User)

web_hook = Recipe(WebHook)