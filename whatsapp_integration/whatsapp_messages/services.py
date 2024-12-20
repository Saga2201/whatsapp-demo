import logging
import os

from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory

from .models import Message

load_dotenv()

AZURE_ENDPOINT = os.environ.get("AZURE_ENDPOINT")
API_KEY = os.environ.get("AZURE_API_KEY")
DEPLOYMENT_NAME = os.environ.get("DEPLOYMENT_NAME")

logger = logging.getLogger('whatsapp_messages')

llm = AzureChatOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=API_KEY,
    openai_api_version="2024-02-15-preview",
    deployment_name=DEPLOYMENT_NAME
)


class MessageService:
    @staticmethod
    def handle_incoming_message(data: dict, ai_response: str) -> Message:
        """
        Handle incoming WhatsApp messages (Webhook).
        """
        logger.info("Handling incoming message with data: %s", data)
        user_id = data.get('user_id')
        sender = data.get('sender')
        receiver = data.get('receiver')
        content = data.get('content')

        if not sender or not receiver or not content:
            raise ValueError("Invalid message data")

        message = Message.objects.create(
            user_id=user_id,
            sender=sender,
            receiver=receiver,
            content=content,
            ai_response=ai_response,
            status='delivered'
        )
        logger.info("Successfully handled incoming message: %s", message)
        return message

    @staticmethod
    def process_outgoing_message(user_id: str, sender: str, receiver: str, content: str, ai_response: str) -> Message:
        """
        Process outgoing WhatsApp messages.
        """
        logger.info("Processing outgoing message. Sender: %s, Receiver: %s", sender, receiver)
        if not sender or not receiver or not content:
            raise ValueError("Missing sender, receiver, or content")

        message = Message.objects.create(
            user_id=user_id,
            sender=sender,
            receiver=receiver,
            content=content,
            ai_response=ai_response,
            status='sent'
        )
        message.status = 'delivered'
        message.save()

        logger.info("Outgoing message created: %s", message)
        return message

    @staticmethod
    def get_last_message(user_id: str) -> Message:
        """
        Get the last message for a user.
        """
        if not user_id:
            raise ValueError("Missing user_id")
        try:
            logger.info("Getting last message for user: %s", user_id)
            return Message.objects.filter(
                user_id=user_id
            ).order_by('-timestamp').values("content", "ai_response")[:5]
        except Exception as e:
            logger.error("Error getting last message for user: %s", e)
            raise ValueError("Error getting last message for user")

    @staticmethod
    def process_and_prepare_buffer_memory(user_id: str) -> ConversationBufferMemory:
        """
        Get all messages for a user. and prepare buffer memory,
        """
        try:
            logger.info("Getting all messages for user: %s", user_id)
            memory = ConversationBufferMemory(memory_key="history")
            messages = MessageService.get_last_message(user_id=user_id)
            for message in messages:
                memory.save_context({"input": message["content"]}, {"output": message["ai_response"]})
            logger.info("Buffer memory created: %s", memory)
            return memory
        except Exception as e:
            logger.error("Error getting messages for user: %s", e)
            raise ValueError("Error getting messages for user")


class LLMWHelper:
    @staticmethod
    def generate_response(prompt: str, user_id: str):
        memory = MessageService.process_and_prepare_buffer_memory(user_id=user_id)
        llm_chain = ConversationChain(llm=llm, verbose=True, memory=memory)
        return llm_chain.invoke(prompt)
