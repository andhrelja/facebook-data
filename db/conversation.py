from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Text,
    ForeignKey
)

from config import Base


class Conversation(Base):
    __tablename__ = 'conversations'

    id        = Column(Integer, primary_key=True, autoincrement=True)
    title     = Column(String(255))

    is_group  = Column(Boolean)
    is_active = Column(Boolean)

    messages  = relationship("Message", back_populates="conversation")
    conversation_participants = relationship("ConversationParticipants", back_populates="conversation")

    def __repr__(self):
        return "<Conversation (title={})>".format(self.title)

    def __str__(self):
        return "<Conversation (title={})>".format(self.title)


class ConversationParticipants(Base):
    __tablename__ = 'conversation_participants'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False, index=True)
    user_id         = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    conversation = relationship("Conversation", back_populates="conversation_participants")
    user = relationship("User", back_populates="conversation_participants")

    def __repr__(self):
        return "<ConversationParticipants (conversation={})>".format(self.conversation.title)

    def __str__(self):
        return "<ConversationParticipants (conversation={})>".format(self.conversation.title)


class Message(Base):
    __tablename__ = 'messages'

    id          = Column(Integer,   primary_key=True, autoincrement=True)
    sender_name = Column(String,    nullable=False)
    content     = Column(Text,      nullable=True)
    timestamp   = Column(DateTime,  nullable=False)
    type        = Column(String,    nullable=True)

    files       = Column(Integer,   nullable=True)
    photos      = Column(Integer,   nullable=True)
    videos      = Column(Integer,   nullable=True)
    audio_files = Column(Integer,   nullable=True)
    reactions   = Column(Integer,   nullable=True)
    gifs        = Column(Integer,   nullable=True)
    
    share       = Column(Integer,   nullable=True)
    missed      = Column(Boolean,   nullable=True)
    call_duration = Column(Integer, nullable=True)

    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False, index=True)
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return "<Message (conversation={})>".format(self.conversation.title)
