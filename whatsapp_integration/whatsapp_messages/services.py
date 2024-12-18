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

# Temporary memory this can be dynamic
memory = ConversationBufferMemory(memory_key="history")
memory.save_context({"input": "My name is Paul"}, {"output": "Ok, i'll remember that"})
memory.save_context({"input": "What is this platform is all about?"},
                    {"output": "This platform is providing AI integration service with any type of chatbot."})


class MessageService:
    @staticmethod
    def handle_incoming_message(data: dict):
        """
        Handle incoming WhatsApp messages (Webhook).
        """
        logger.info("Handling incoming message with data: %s", data)
        sender = data.get('sender')
        receiver = data.get('receiver')
        content = data.get('content')

        if not sender or not receiver or not content:
            raise ValueError("Invalid message data")

        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content,
            status='delivered'
        )
        logger.info("Successfully handled incoming message: %s", message)
        return message

    @staticmethod
    def process_outgoing_message(sender, receiver, content):
        """
        Process outgoing WhatsApp messages.
        """
        logger.info("Processing outgoing message. Sender: %s, Receiver: %s", sender, receiver)
        if not sender or not receiver or not content:
            raise ValueError("Missing sender, receiver, or content")

        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content,
            status='sent'
        )
        message.status = 'delivered'
        message.save()

        logger.info("Outgoing message created: %s", message)
        return message


class LLMWHelper:
    @staticmethod
    def generate_response(prompt):
        llm_chain = ConversationChain(llm=llm, verbose=True, memory=memory)
        return llm_chain.invoke(prompt)

    @staticmethod
    def generate_response_with_context(prompt, context):
        return llm.invoke(prompt, context)
