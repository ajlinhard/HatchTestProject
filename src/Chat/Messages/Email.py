
from .MessageRegistry import MessageRegistry
from src.Backend.ColumnEnums import MessageType

@MessageRegistry.register(MessageType.EMAIL)
class Email():
    """
    Email Provider class for sending and receiving Email messages. 
    NOTE: with more time this could be an abstract class for Email providers.
    """

    def __init__(self, base_url: str='www.mailplus.app/api/email', api_key: str='test'):
        self.base_url = base_url
        self.api_key = api_key # this would be a secret in a real app


    def send_message(self, message: str):
        """
        Send an Email message.
        """
        # Here you would implement the actual API call to send the Email
        # For example, using requests library:
        # response = requests.post(f"{self.base_url}/send", data={"to": to, "message": message}, headers={"Authorization": f"Bearer {self.api_key}"})
        # return response.json()
        pass

    def receive_message(self):
        """
        Receive an Email message.
        """
        # Here you would implement an specific actions you want to happen when this type of message is received.
        pass