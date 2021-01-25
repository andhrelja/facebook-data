from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey
)

from config import Base


class Comment(Base):
    __tablename__ = 'comments'

    id          = Column(Integer, primary_key=True, autoincrement=True)
    content     = Column(Text)
    author      = Column(String(255))
    target_post = Column(String(255))
    group       = Column(String(255))
    timestamp   = Column(DateTime)

    author_id   = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    author = relationship("User", back_populates="comment_authors", foreign_keys=[author_id], sync_backref=False)

    target_id   = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    target_user = relationship("User", back_populates="comment_targets", foreign_keys=[target_id], sync_backref=False)

    group_id    = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    group = relationship("User", back_populates="comment_groups", foreign_keys=[group_id], sync_backref=False)

    
    def __repr__(self):
        return "<Comment (name={})>".format(self.name)

    def __str__(self):
        return "<Comment (name={})>".format(self.name)
