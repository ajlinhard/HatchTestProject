
from enum import Enum
import json
from typing import Any, Dict, List, Optional, Union

#These definitions are based on the requirements of different message types in the chat application.
class MessageType(str, Enum):
    SMS = "sms"
    MMS = "mms"
    EMAIL = "email"
    VOICE = "voice"
    VOICEMAIL = "voicemail"

class MessageStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    RECEIVED = "received"