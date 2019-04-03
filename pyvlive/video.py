import datetime


class Video:
    EMBED_CODE = '<iframe src=https://www.vlive.tv/embed/%s?autoPlay=false" ' \
                 'frameborder="no" scrolling="no" marginwidth="0" marginheight="0" ' \
                 'WIDTH="544" HEIGHT="306" allowfullscreen></iframe>'

    def __init__(self, video_seq, title, channel_name, date_time):
        self.video_seq = video_seq
        self.title = title
        self.channel_name = channel_name
        self.datetime = date_time
        self.timestamp = None

    def __str__(self):
        string = 'Title: %s(%s)\nChannel: %s\nTime: %s(%s)\n' \
                 % (
                     self.title,
                     self.video_seq,
                     self.channel_name,
                     self.datetime,
                     self.timestamp
                 )
        return string

    def generate_timestamp(self):
        time_object = datetime.datetime.strptime(self.datetime, '%Y-%m-%d %H:%M:%S')
        self.timestamp = int(time_object.timestamp())

    def generate_embed_code(self):
        return self.EMBED_CODE % self.video_seq
