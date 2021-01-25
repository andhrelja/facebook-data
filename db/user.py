from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String
)

from .comment import Comment
from config import Base


class User(Base):
    __tablename__ = 'users'

    id        = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255))
    username  = Column(String(255))

    conversation_participants = relationship("ConversationParticipants", back_populates="user")
    comment_authors       = relationship("Comment", foreign_keys=[Comment.author_id])
    comment_targets       = relationship("Comment", foreign_keys=[Comment.target_id])
    comment_groups        = relationship("Comment", foreign_keys=[Comment.group_id])

    def __repr__(self):
        return "<User (name={})>".format(self.full_name)

    def __str__(self):
        return "<User (name={})>".format(self.full_name)
