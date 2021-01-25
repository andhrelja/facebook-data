from datetime import datetime

from config import DEBUG

class Conversation(dict):
    def __init__(self, participants, title, group, messages, conversation_data):
        self.participants = participants
        self.title = title
        self.group = group
        self.conversation_data = conversation_data
        self.json_messages = messages
        self.messages = list()

        self.set_messages()
        if DEBUG is True:
            self.print_info()
    
    def set_messages(self):
        for message in self.json_messages:
            self.messages.append(Message(conversation=self, **message))
    
    def print_info(self):
        print(self.__dict__)
    
    def __repr__(self):
        return "<Conversation (title={})>".format(self.title)
    
    def __str__(self):
        return "<Conversation (title={})>".format(self.title)


class Message(dict):
    def __init__(self,
        conversation,
        sender_name,
        timestamp_ms,
        type,
        content=str(),
        files=list(),
        photos=list(),
        videos=list(),
        reactions=list(),
        gifs=list(),
        users=None,
        sticker=None,
        audio_files=None,
        missed=None,
        share=None,
        call_duration=None,
        ip=None
    ):
        self.conversation   = conversation
        self.sender_name    = sender_name if sender_name != "" else "Korisnik Facebooka"
        self.type           = type
        self.content        = content
        self.files          = files
        self.photos         = photos
        self.videos         = videos
        self.reactions      = reactions
        self.gifs           = gifs
        self.users          = users
        self.sticker        = sticker
        self.audio_files    = audio_files
        self.missed         = missed
        self.share          = share
        self.call_duration  = call_duration
        self.ip             = ip

        if isinstance(timestamp_ms, int):
            ts = timestamp_ms / 1000
            self.timestamp = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.timestamp = timestamp_ms

    def __repr__(self):
        return "<Message (conversation={})>".format(self.conversation.title)
    
    def __str__(self):
        return "<Message (conversation={})>".format(self.conversation.title)
