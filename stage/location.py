from datetime import datetime


class Location(dict):
    def __init__(self, name, latitude, longitude, timestamp):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


    def __repr__(self):
        return "<Location (name={})>".format(self.name)
    
    def __str__(self):
        return "<Location (name={})>".format(self.name)
