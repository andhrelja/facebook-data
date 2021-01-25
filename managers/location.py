from db.location import Location

from progress.bar import Bar


class LocationManager(object):
    def __init__(self, session=None, locations=None):
        self.session = session
        self.locations = locations
    
    def ingest_all(self):
        if self.session:
            self.ingest_locations()
        else:
            raise AttributeError('Session is not set')
    
    def ingest_locations(self):
        bar = Bar('Ingesting locations', max=len(self.locations))
        for location in self.locations:
            location = Location(**location.__dict__)
            self.session.add(location)
            bar.next()
        self.session.commit()
        bar.finish()
