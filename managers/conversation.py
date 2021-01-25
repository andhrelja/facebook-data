from db.conversation import Conversation, ConversationParticipants, Message
from db.user import User

from datetime import datetime
from progress.bar import Bar


length = lambda lst: 0 if not lst else len(lst)
get_username = lambda full_name: full_name.replace(' ', '_').lower()


class ConversationManager(object):
    def __init__(self, session=None, conversations=None):
        self.session = session
        self.conversations = conversations
    
    def ingest_all(self):
        if self.session:
            self.ingest_users()
            self.ingest_conversations()
        else:
            raise AttributeError('Session is not set')
    
    def get_distinct_participants(self):
        participants = set()
        for conversation in self.conversations:
            participants = participants.union(conversation.participants)
        return participants
    
    def ingest_users(self):
        participants = self.get_distinct_participants()
        bar = Bar('Ingesting users', max=len(participants))
        for participant in participants:
            user = User(full_name=participant, username=get_username(participant))
            self.session.add(user)
            bar.next()
        self.session.commit()
        bar.finish()

    def ingest_conversations(self):
        bar = Bar('Ingesting conversations', max=len(self.conversations))

        for conversation in self.conversations:
            is_active = True
            if conversation.title == "Korisnik Facebooka":
                is_active = False

            conv = Conversation(
                title=conversation.title, 
                is_group=conversation.group,
                is_active=is_active
            )

            self.session.add(conv)
            self.session.commit()

            self.ingest_conversation_participants(conv.id, conversation)    
            self.ingest_messages(conv.id, conversation)
            bar.next()
        bar.finish()
    
    def ingest_conversation_participants(self, conversation_id, conversation):
        conversation_participants = list()
        for participant in conversation.participants:
            users = self.session.query(User).filter(User.full_name == participant)
            user = users.first()
            conversation_participant = ConversationParticipants(conversation_id=conversation_id, user_id=user.id)
            conversation_participants.append(conversation_participant)
        
        self.session.add_all(conversation_participants)
        self.session.commit()


    def ingest_messages(self, conversation_id, conversation):
        messages = list()
        for message in conversation.messages:
            timestamp = datetime.strptime(message.timestamp, '%Y-%m-%d %H:%M:%S')
            message = Message(
                sender_name=message.sender_name,
                content=message.content,
                timestamp=timestamp,
                type=message.type,
                files=length(message.files),
                photos=length(message.photos),
                videos=length(message.videos),
                audio_files=length(message.audio_files),
                reactions=length(message.reactions),
                gifs=length(message.gifs),
                share=length(message.share),
                missed=message.missed,
                call_duration=message.call_duration,
                conversation_id=conversation_id
            )
            messages.append(message)
        
        self.session.add_all(messages)
        self.session.commit()

