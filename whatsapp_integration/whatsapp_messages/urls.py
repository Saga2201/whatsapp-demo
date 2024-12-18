from django.urls import path
from .views import WebhookView, SendMessageView

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook'),
    path('send-message/', SendMessageView.as_view(), name='send_message'),
]
