# coding=utf-8

class Track:
    def __init__(self, artist, name, json, duration, path):
        self.artist = artist
        self.name = name
        self.json = json
        self.duration = duration
        self.path = path

    def __str__(self):
        return '%s - %s [%s]' % (self.artist.encode('utf-8'), self.name.encode('utf-8'),
                                 self.duration.encode('utf-8'))
