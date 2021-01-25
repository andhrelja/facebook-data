from db.conversation import Conversation, ConversationParticipants, Message
from managers.conversation import ConversationManager
from managers.location import LocationManager
from managers.comment import CommentManager

from parsers.conversation import ConversationParser
from parsers.location import LocationParser
from parsers.comment import CommentParser

from db.location import Location
from db.comment import Comment

from sqlalchemy.orm import sessionmaker
from config import Base, engine


# TODO: Friends (current + removed)
# TODO: Posts

Session = sessionmaker(bind=engine)

def get_conversations():
    parser = ConversationParser()
    parser.set_conversations()
    return parser.conversations

def get_locations():
    parser = LocationParser()
    parser.set_locations()
    return parser.locations

def get_comments():
    parser = CommentParser()
    parser.set_comments()
    return parser.comments

def db_create_all(creates):
    for Table in creates:
        Table.__table__.create()

def db_drop_all(drops):
    for Table in drops:
        Table.__table__.drop()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    create = [Conversation, ConversationParticipants, Message]
    drop = [Conversation, ConversationParticipants, Message]

    create = [Location]
    drop = [Location]

    

    """
    conversations = get_conversations()
    manager = ConversationManager(session, conversations)
    manager.ingest_all()

    locations = get_locations()
    manager = LocationManager(session, locations)
    manager.ingest_all()
    """

    create = [Comment]
    drop = [Comment]

    db_drop_all(drop)
    db_create_all(create)

    comments = get_comments()
    manager = CommentManager(session, comments)
    manager.set_target_users()
    manager.set_authors()
    manager.ingest_all()
