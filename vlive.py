import requests
import datetime


class channel():
    VLIVE_URI = (
        'https://api-vfan.vlive.tv/vproxy/channelplus/getChannelVideoList'
        '?app_id=%(app_id)s'
        '&channelSeq=%(channelSeq)s'
        '&maxNumOfRows=%(maxNumOfRows)s'
        '&pageNo=%(pageNo)s'
    )
    VFAN_APP_ID = '8c6cc7b45d2568fb668be6e05b6e5a3b'
    MAX_NUM_LIST = 100


    def __init__(self, channel_seq):
        self.channel_seq = channel_seq
        self.video_list = []
        self.page = 1
        self.index = 0
        self.configure_video_list()


    def __iter__(self):
        return self


    def __next__(self):
        if self.index >= len(self.video_list):
            raise StopIteration
        self.set_timestamp()
        content = self.video_list[self.index]
        self.index += 1
        return content


    def fetch_video_list(self):
        uri = self.VLIVE_URI % {
            'app_id': self.VFAN_APP_ID,
            'channelSeq': self.channel_seq,
            'maxNumOfRows': self.MAX_NUM_LIST,
            'pageNo': self.page
        }
        res = requests.get(uri)
        data = res.json()
        return data


    def configure_video_list(self):
        data = self.fetch_video_list()['result']
        for i in data['videoList']:
            content = {
                'video_seq': str(i['videoSeq']),
                'title': i['title'],
                'time': i['onAirStartAt']
            }
            self.video_list.append(content)
        total = data['totalVideoCount']
        if total-(self.page)*100 > 0:
            self.page += 1
            self.configure_video_list()


    def set_timestamp(self):
        self.video_list[self.index]['timestamp'] = generate_timestamp(self.video_list[self.index]['time'])


class embed_code():
    EMBED_CODE = '<iframe src=https://www.vlive.tv/embed/%s?autoPlay=false" frameborder="no" scrolling="no" marginwidth="0" marginheight="0" WIDTH="544" HEIGHT="306" allowfullscreen></iframe>'


    def __new__(cls, video_seq):
        return cls.EMBED_CODE%(video_seq)


def generate_timestamp(time):
    time_object = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    timestamp = int(time_object.timestamp())
    return timestamp