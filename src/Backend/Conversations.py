import os
import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Union

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel, Field

# Internal Package Imports
from .ColumnEnums import MessageType, MessageStatus
from src.sys_configs import Configs

# Database setup
DATABASE_URL = Configs.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Stores the individual messages sent to and from the customer. This is the main table for the message history.
class MessagesLog(Base):
    __tablename__ = "messages_log"

    msg_id = Column(Integer, primary_key=True)
    conv_id = Column(Integer, ForeignKey("conversations_log.conv_id"), index=True) # Index the conv_id since history will be pulled often by this.
    msg_from = Column(String(255), nullable=False)
    msg_to = Column(String(255), nullable=False)
    msg_type = Column(String(50), nullable=False, default=MessageType.SMS)
    msg_status = Column(String(50), nullable=False, default=MessageStatus.PENDING)
    msg_provider_id = Column(String(100), nullable=True)
    msg_body = Column(Text, nullable=False)
    msg_attachments = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.now)

# Stores the information representing an entire converstation between the customer and client.
class ConversationLog(Base):
    __tablename__ = "conversations_log"
    
    conv_id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=lambda: str(uuid.uuid4()), unique=True, index=True)
    client_id = Column(Integer, nullable=False)
    # client_id = Column(Integer, ForeignKey("clients.client_id"))
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    

# A table for validation of clients in the entire Hatch system.

class Clients(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(255), nullable=False)
    client_type = Column(String(50), nullable=False)
    client_active_fl = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)