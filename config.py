import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DEBUG = False

FACEBOOK_DATA_DIR = os.path.join('C:/Users/andhr/Documents/Facebook Data')
MESSAGES_DIR = os.path.join(FACEBOOK_DATA_DIR, 'messages')
LOCATIONS_DIR = os.path.join(FACEBOOK_DATA_DIR, 'location')
COMMENTS_DIR = os.path.join(FACEBOOK_DATA_DIR, 'comments')

MESSAGES_OUTPUT = os.path.join('conversations.json')
LOCATIONS_OUTPUT = os.path.join('locations.json')
COMMENTS_OUTPUT = os.path.join('comments.json')

engine = create_engine('postgresql://andrea:user@localhost/facebookdata', echo=False)
Base = declarative_base(bind=engine)
