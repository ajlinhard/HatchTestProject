from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
import json
import time
from datetime import datetime
from requests.exceptions import HTTPError

# Internal Package Imports
from src.sys_configs import Configs
from src.Backend.Conversations import Base, ConversationLog, MessagesLog
from src.Backend.ColumnEnums import MessageType, MessageStatus
from src.Chat.Messages.MessageRegistry import MessageRegistry

class Conversation:
    def __init__(self):
        self.conv_id = None
        self.ls_message_history = []
        # Initialize the database connection
        self.db_engine = create_engine(Configs.DATABASE_URL)
        Base.metadata.create_all(self.db_engine)
        self.SessionLocal = sessionmaker(bind=self.db_engine)
        self.session = self.SessionLocal()

        # Initialize ConversationLog and grab history if conv_id is provided
        self.initialize()

    def initialize(self, contact_info:str = None):
        if contact_info:
            self.conv_id = self.existing_conversation(contact_info)
            print(f"Conversation ID: {self.conv_id}")
        # Logic to initialize a ConversationLog
        if self.conv_id is not None:
            # Fetch ConversationLog details from the database
            new_ConversationLog = self.session.query(ConversationLog).filter(ConversationLog.conv_id == self.conv_id).first()
            if not new_ConversationLog:
                raise ValueError(f"ConversationLog ID {self.conv_id} was not found, in the histroy. Please start a new ConversationLog.")
        else:
            # Create a new ConversationLog
            new_ConversationLog = ConversationLog(
                client_id=1,  # Replace with actual client ID
                title=f"New ConversationLog ({str(uuid4())})"  # Replace with actual title if needed
            )
            self.session.add(new_ConversationLog)
            self.session.commit()
            self.conv_id = new_ConversationLog.conv_id

    def existing_conversation(self, contact_info:str):
        if not isinstance(contact_info, str):
            raise ValueError(f"contact_info must be a string of data not a {type(contact_info)}.")
        # Logic to check if a conversation already exists
        msg_logs = self.session.query(MessagesLog).filter(MessagesLog.msg_to == contact_info).first()
        return msg_logs.conv_id if msg_logs else None


    def create(self, from_:str, to:str, body:str, type: str = MessageType.EMAIL, messaging_provider_id: str = None, attachments= None):
        # Logic to create a message
        message = {
            "from": from_,
            "to": to,
            "type": type,
            "body": body,
            "messaging_provider_id": messaging_provider_id,
            "attachments": attachments,
            "timestamp": datetime.now()
            }
        return self.send_message(message)

    def send_message(self, message, max_retries=3):
        # Logic to send a message
        if not isinstance(message,dict):
            message = json.loads(message.decode('utf-8'))
        msg_type = message.get('type', 'email')
        msg_obj = MessageRegistry.get_provider(msg_type)()
        print(type(msg_obj))
        retry_count = 0
        retry_after = 2  # seconds to wait before retrying
        error_obj = None
        while retry_count <= max_retries:
            try:
                msg_obj.send_message(
                    message=message
                )
                break  # Exit the loop if the message is sent successfully
            except HTTPError as http_err:
                status_code = http_err.response.status_code
                error_obj = http_err
                if status_code == 400:
                    # Consider logging the request details for debugging
                    raise ValueError("Malformed request. Please check your request parameters.") from http_err
                    
                elif status_code == 401:
                    # You might want to refresh tokens here if using OAuth
                    raise PermissionError("Authentication failed. Please check your credentials.") from http_err
                    
                elif status_code == 403:
                    raise PermissionError("You don't have permission to access this resource.") from http_err
                    
                elif status_code == 404:
                    raise FileNotFoundError(f"The requested resource was not found.") from http_err
                    
                elif status_code == 429:
                    retry_count += 1
                    
                    # Check if we've exceeded the maximum number of retries
                    if retry_count > max_retries:
                        raise RuntimeError("Retry rate limit exceeded. Please try again later.") from http_err
                    
                    time.sleep(retry_after)
                    continue  # Retry the request
                else:
                    # Handle any other HTTP errors
                    raise http_err
                    
            except Exception as err:
                # Handle non-HTTP errors (network issues, timeouts, etc.)
                error_obj = err
                raise
            # Log the results of the message being sent
            finally:
                # Update the message status in the database
                new_message = MessagesLog(
                    conv_id=self.conv_id,
                    msg_from=message.get('from'),
                    msg_to=message.get('to'),
                    msg_type=msg_type,
                    msg_provider_id=message.get('messaging_provider_id', None),
                    msg_attachments=message.get('attachments'),
                    msg_status=MessageStatus.SENT if error_obj is None else MessageStatus.FAILED,
                    msg_body=message.get('body')
                )
                self.session.add(new_message)
                self.session.commit()

    def receive_message(self, message):
        # Logic to receive a message
        if isinstance(message,str):
            message = json.loads(message)
        msg_type = message.get('type', 'email')
        msg_obj = MessageRegistry.get_provider(msg_type)()
        error_obj = None
        # Try and process the message received
        try:
            response = msg_obj.receive_message()
            if not isinstance(response,dict) and response is not None:
                response = json.loads(message.decode('utf-8'))
        except Exception as e:
            raise ValueError(f"Failed to receive message: {e}")
        # Log the results of the message received
        finally:
            new_message = MessagesLog(
                conv_id=self.conv_id,
                msg_from=message.get('from'),
                msg_to=message.get('to'),
                msg_type=msg_type,
                msg_provider_id=message.get('messaging_provider_id', message.get('xillio_id')),
                msg_attachments=message.get('attachments'),
                msg_status=MessageStatus.RECEIVED if error_obj is None else MessageStatus.FAILED,
                msg_body=message.get('body')
            )
            self.session.add(new_message)
            self.session.commit()

    def print_chat_history(self):
        # Logic to print chat history
        ls_message_history = self.session.query(MessagesLog).filter(MessagesLog.conv_id == self.conv_id).all()
        for message in self.ls_message_history:
            print(f"{message['from']}: {message['message']}")