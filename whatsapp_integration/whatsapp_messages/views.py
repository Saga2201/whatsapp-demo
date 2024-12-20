import logging

from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MessageSerializer
from .services import MessageService, LLMWHelper

logger = logging.getLogger('whatsapp_messages')


class WebhookView(APIView):
    """
    Webhook endpoint for receiving WhatsApp messages.
    """

    @atomic
    def post(self, request):
        logger.info("Webhook received data: %s", request.data)
        try:
            llm_response = LLMWHelper.generate_response(request.get('sender'), request.data("user_id"))
            ai_response = llm_response.get("response") if isinstance(llm_response, dict) else llm_response.content
            message = MessageService.handle_incoming_message(request.data, ai_response)
            serializer = MessageSerializer(message)
            logger.info("Incoming message processed successfully: %s", message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            logger.error("Error handling incoming message: %s", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendMessageView(APIView):
    """
    Endpoint for sending WhatsApp messages.
    """

    @atomic
    def post(self, request):
        logger.info("SendMessage API called with data: %s", request.data)
        try:
            user_id = request.data.get('user_id')
            sender = request.data.get('sender')
            receiver = request.data.get('receiver')
            content = request.data.get('content')
            llm_response = LLMWHelper.generate_response(content, user_id)
            ai_response = llm_response.get("response") if isinstance(llm_response, dict) else llm_response.content
            message = MessageService.process_outgoing_message(user_id, sender, receiver, content, ai_response)

            serializer = MessageSerializer(message)

            logger.info("Outgoing message sent successfully: %s", message)
            serializer_data = serializer.data
            return Response(serializer_data, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error("Error sending outgoing message: %s", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
