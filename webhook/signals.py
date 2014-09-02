import django.dispatch

# signal
webhook_triggered_signal = django.dispatch.Signal(
    providing_args=['triggered', 'action', 'content_object', 'content_type'])