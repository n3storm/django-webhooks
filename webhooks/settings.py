from django.conf import settings

# App Defaults
WEB_HOOK_OWNER_MODEL = 'django.contrib.auth.models.User'
WEB_HOOK_ACTIONS = ()
WEB_HOOK_OWNER_LOCAL = True  # Do we get owner from account() or from content_object() ?

# Override defaults, if defined in django project settings
WEB_HOOK_OWNER_MODEL = getattr(settings, 'WEB_HOOK_OWNER_MODEL', WEB_HOOK_OWNER_MODEL)
WEB_HOOK_ACTIONS = getattr(settings, 'WEB_HOOK_ACTIONS', WEB_HOOK_ACTIONS)
WEB_HOOK_OWNER_LOCAL = getattr(settings, 'WEB_HOOK_OWNER_LOCAL', WEB_HOOK_OWNER_LOCAL)

# Work out our dynamic relation. Nb. Django 1.7 has a function to do this. (django.utils.importlib import_module)
app_name = WEB_HOOK_OWNER_MODEL.rsplit('.', 1)[0]
model_name = WEB_HOOK_OWNER_MODEL.rsplit('.', 1)[1]
module = __import__(app_name, fromlist=[model_name])
OWNER_MODEL = getattr(module, model_name)