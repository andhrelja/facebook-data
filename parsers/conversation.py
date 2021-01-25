import os
from progress.bar import Bar

from stage.conversation import Conversation
from config import MESSAGES_DIR, MESSAGES_OUTPUT
from utils import read_initial_json, read_json, write_json


class ConversationParser(object):

    def __init__(self, inbox_dir='inbox'):
        self.inbox_dir = os.path.join(MESSAGES_DIR, inbox_dir)
        self.conversation_data = list()
        self.conversations = list()
    
    def set_conversations(self, limit=None):
        if not os.path.isfile(MESSAGES_OUTPUT):
            conversations = self.collect_conversations(limit)
            self._set_conversations(conversations)
            self.write_to_json()
        else:
            conversations = read_json(MESSAGES_OUTPUT)
            self._set_conversations(conversations[:limit])

    def _set_conversations(self, conversations):
        bar = Bar('Setting up conversations', max=len(conversations))
        for conversation in conversations:
            self.conversation_data.append(conversation)
            self.conversations.append(Conversation(conversation_data=conversation, **conversation))
            bar.next()
        bar.finish()

    def collect_conversations(self, limit):
        conversations = list()
        conversation_folders = os.listdir(self.inbox_dir)[:limit]

        bar = Bar('Collecting conversations', max=len(conversation_folders))
        for folder in conversation_folders:
            conversation = self._collect_conversations(os.path.join(self.inbox_dir, folder))
            conversations.append(conversation)
            bar.next()
        bar.finish()
        return conversations
    
    def _collect_conversations(self, conversation_directory):
        conversation = {
            'participants': set(),
            'title': str(),
            'group': bool(),
            'messages': list(),
        }

        # Read multiple message.json files (message_1.json and message_2.json)
        for _filename in os.listdir(conversation_directory):
            filepath = os.path.join(conversation_directory, _filename)
            if os.path.isfile(filepath) and _filename.startswith('message'):
                conversation_data = self._collect_conversation_data(filepath)
                conversation['participants'] = conversation['participants'].union(conversation_data['participants'])
                conversation['title'] = conversation_data['title'] if conversation_data['title'] != "" else "Korisnik Facebooka"
                conversation['group'] = conversation_data['group']
                conversation['messages'] += conversation_data['messages']
        
        conversation['participants'] = list(conversation['participants'])
        return conversation
    
    def _collect_conversation_data(self, path):
        participants = list()
        title = str()
        group = bool()
        messages = list()

        dict_from_json = read_initial_json(path)
        for participant in dict_from_json['participants']:
            participants.append(participant['name'])
        title = dict_from_json['title']

        if dict_from_json['thread_type'] == 'Regular':
            group = False
        else:
            group = True
                
        messages = dict_from_json['messages']
        return dict(participants=participants, messages=messages, title=title, group=group)

    def write_to_json(self):
        write_json(MESSAGES_OUTPUT, self.conversation_data)
    