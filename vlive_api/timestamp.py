import datetime


def generate_timestamp(time):
    time_object = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    timestamp = int(time_object.timestamp())
    return timestamp