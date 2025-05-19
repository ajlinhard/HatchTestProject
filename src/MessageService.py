from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
import json
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Internal Package Imports
from src.sys_configs import Configs
from Backend.Conversations import Base, ConversationLog, MessagesLog
from Backend.ColumnEnums import MessageType, MessageStatus
from Chat.Messages.MessageRegistry import MessageRegistry
from Chat.Conversation import Conversation


class MessageService:
    def __init__(self, name:str):
        self.app = Flask(name)
        self.app.config['JSON_AS_ASCII'] = False
        self.app.config['JSONIFY_MIMETYPE'] = 'application/json'
        self.configure_routes()
        self.conversation = Conversation()
        # Initialize the database connection
        self.db_engine = create_engine(Configs.DATABASE_URL)
        Base.metadata.create_all(self.db_engine)
        self.SessionLocal = sessionmaker(bind=self.db_engine)
        self.session = self.SessionLocal()

    def configure_routes(self):
        # Define all your routes
        self.app.add_url_rule('/send', 'send', self.send, methods=['POST'])
        self.app.add_url_rule('/receive', 'receive', self.receive, methods=['POST'])

    def run(self, debug=True):
        self.app.run(host='0.0.0.0', port=5000, debug=debug)
    
    def send(self):
        """Send a message to the customer."""
        data = request.json
        print(data.get('to'))
        self.conversation.initialize(data.get('to'))
        self.conversation.send_message(data)
        return jsonify({
                'message': 'Message sent successfully',
            })

    def receive(self):
        """Receive a response message from the customer."""
        data = request.json
        self.conversation.initialize(data.get('from'))
        self.conversation.receive_message(data)
        return jsonify({
                'message': 'Message received successfully',
            })


# Create and run the application
if __name__ == '__main__':
    flask_app = MessageService("test_App")
    flask_app.run(debug=True)