
import requests
from requests.exceptions import HTTPError
import logging

from .MessageRegistry import MessageRegistry
from src.Backend.ColumnEnums import MessageType

@MessageRegistry.register(MessageType.SMS)
class SMS():
    """
    SMS Provider class for sending and receiving SMS messages. 
    NOTE: with more time this could be an abstract class for SMS providers.
    """

    def __init__(self, base_url: str='www.provider.app/api/messages', api_key: str = 'test'):
        self.base_url = base_url
        self.api_key = api_key # this would be a secret in a real app
        self.provider_id = 1

    def send_message(self, message: dict):
        """
        Send an SMS message.
        """
        # Here you would implement the actual API call to send the SMS
        # For example, using requests library:
        if self.api_key == 'test':
            return {"msg_status": "sent"}
        else:
            response = requests.post(f"{self.base_url}/send", data= message, headers={"Authorization": f"Bearer {self.api_key}"})
            return response.json()

    def receive_message(self):
        """
        Receive an SMS message.
        """
        # Here you would implement an specific actions you want to happen when this type of message is received.
        pass