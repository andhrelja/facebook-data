import os
from progress.bar import Bar

from stage.location import Location
from config import LOCATIONS_DIR, LOCATIONS_OUTPUT
from utils import read_initial_json, read_json, write_json


class LocationParser(object):
    def __init__(self, locations_dir='location_history.json'):
        self.locations_dir = os.path.join(LOCATIONS_DIR, locations_dir)
        self.location_data = list()
        self.locations = list()
    
    def set_locations(self, limit=None):
        if not os.path.isfile(LOCATIONS_OUTPUT):
            locations = self.collect_locations(limit)
            self._set_locations(locations)
            self.write_to_json()
        else:
            locations = read_json(LOCATIONS_OUTPUT)
            self._set_locations(locations[:limit])

    def _set_locations(self, locations):
        bar = Bar('Setting up locations', max=len(locations))

        for location in locations:
            loc = Location(**location)
            self.locations.append(loc)
            self.location_data.append(location)
            bar.next()
        
        bar.finish()

    def collect_locations(self, limit):
        locations = list()

        location_data = read_initial_json(self.locations_dir)
        location_list = location_data['location_history'][:limit]

        bar = Bar('Collecting locations', max=len(location_list))
        for location in location_list:
            location = self._collect_location_data(location)
            locations.append(location)
            bar.next()
        bar.finish()
        return locations
    
    def _collect_location_data(self, location):
        _location = {
            'name' : location['name'],
            'latitude' : location['coordinate']['latitude'],
            'longitude' : location['coordinate']['longitude'],
            'timestamp' : location['creation_timestamp'],
        }

        return _location

    def write_to_json(self):
        write_json(LOCATIONS_OUTPUT, self.location_data)
    