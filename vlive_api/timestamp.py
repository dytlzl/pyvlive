import datetime


class generate_timestamp():
    def __new__(cls, time):
        time_object = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        timestamp = int(time_object.timestamp())
        return timestamp