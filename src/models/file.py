import datetime
import time

class File():
    def __init__(self, name, size, date):
        self.name = name
        self.size = size
        self.date = self.set_date(date[0], date[1])

    def set_date(self, date, time):
        # Split and convert date to int list
        d = [int(x) for x in date.split("-")]
        # Round seconds
        t = time.split(":")
        t[2] = t[2].split(".")[0]
        t = [int(x) for x in t]
        return datetime.datetime(d[0], d[2], d[1], t[0], t[1], t[2])

    def serialize(self):
        return {
            'name': self.name, 
            'size': self.size,
            'date': self.date,
        }
