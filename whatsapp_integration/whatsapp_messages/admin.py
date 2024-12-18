from django.contrib import admin
from .models import Message
import logging

logger = logging.getLogger('whatsapp_messages')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Custom admin interface for managing messages.
    """
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'status')
    search_fields = ('sender', 'receiver', 'content')
    list_filter = ('status', 'timestamp')
    actions = ['send_test_message']

    def get_actions(self, request):
        """
        Override get_actions to log available actions during runtime.
        """
        actions = super().get_actions(request)
        logger.debug("Available actions: %s", actions.keys())
        return actions

    def send_test_message(self, request, queryset):
        """
        Admin action to send test messages.
        """
        try:
            for message in queryset:
                logger.info(f"Sending test message: {message}")
                message.status = 'sent'
                message.save()
            self.message_user(request, "Test messages sent successfully.")
        except Exception as e:
            logger.error(f"Error sending test messages: {e}")
            self.message_user(request, "Failed to send test messages.", level='error')

    send_test_message.short_description = "Send Test Message to Selected"
