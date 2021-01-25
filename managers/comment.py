import os
import textdistance
from progress.bar import Bar

from db.comment import Comment
from db.user import User
from utils import read_json, write_json


class CommentManager(object):
    def __init__(self, session=None, comments=None):
        self.session = session
        self.comments = comments
    
    def ingest_all(self):
        if self.session:
            self.ingest_comments()
        else:
            raise AttributeError('Session is not set')
    
    def ingest_comments(self):
        bar = Bar('Ingesting comments', max=len(self.comments))
        for comment in self.comments:
            comment = Comment(**comment.to_dict())
            self.session.add(comment)
            bar.next()
        self.session.commit()
        bar.finish()

    
    def get_distinct_target_users(self):
        users = set()
        for comment in self.comments:
            if comment.target_user is not None:
                users.add(comment.target_user)
        return users

    def get_target_full_name(self, users, target_user):
        for user in users:
            distance = textdistance.levenshtein.normalized_similarity(user.full_name, target_user)
            if distance > 0.8:
                return user.full_name

    def get_target_users_mapping(self):
        if os.path.isfile('target_users.json'):
            return read_json('target_users.json')
        else:
            target_mapping = dict()
            target_users = self.get_distinct_target_users()
            users = self.session.query(User).all()
            bar = Bar('Setting target users mapping (Lev)', max=len(target_users))
            for target_user in target_users:
                user_full_name = self.get_target_full_name(users, target_user)
                target_mapping[target_user] = user_full_name
                bar.next()
            bar.finish()
            write_json('target_users.json', target_mapping)
            return target_mapping
        
    def set_target_users(self):
        target_mapping = self.get_target_users_mapping()
        bar = Bar('Setting comment target users', max=len(self.comments))
        for comment in self.comments:
            try:
                user_full_name = target_mapping[comment.target_user]
            except KeyError: # None
                pass
            else:
                users = self.session.query(User).filter(User.full_name == user_full_name)
                user = users.first()
                comment.target_user = user
            bar.next()
        bar.finish()
    
    def set_authors(self):
        bar = Bar('Setting comment authors', max=len(self.comments))
        for comment in self.comments:
            users = self.session.query(User).filter(User.full_name == comment.author)
            user = users.first()
            comment.author = user
            bar.next()
        bar.finish()
    