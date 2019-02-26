import requests
from .timestamp import generate_timestamp

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


    def __init__(self, channel_seq, limit=1024, allow_other_channel=True, allow_mini_replay=True, search_word=''):
        self.channel_seq = channel_seq
        self.channel_name = ''
        self.video_list = []
        self.limit = limit
        self.allow_other_channel = allow_other_channel
        self.allow_mini_replay = allow_mini_replay
        self.search_word = search_word
        self.page = 1
        self.index = 0


    def __iter__(self):
        return self


    def __next__(self):
        while True:
            if self.can_stop_iteration():
                raise StopIteration
            if self.filter_video_data():
                break
        self.configure_timestamp()
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
        self.channel_name = data['channelInfo']['channelName']
        try:
            for i in data['videoList']:
                video_data = {
                    'video_seq': str(i['videoSeq']),
                    'title': i['title'],
                    'channel_name': i['representChannelName'],
                    'time': i['onAirStartAt']
                }
                self.video_list.append(video_data)
        except KeyError:
            return False
        self.page += 1
        return True


    def filter_video_data(self):
        try:
            if (self.search_word == '' or self.search_word in self.video_list[self.index]['title']
            ) and (self.allow_mini_replay or not '[CH+ mini replay]' in self.video_list[self.index]['title']
            ) and (self.allow_other_channel or self.channel_name == self.video_list[self.index]['channel_name']):
                return True
        except IndexError:
            return False
        self.index += 1
        self.limit += 1
        self.filter_video_data()


    def can_stop_iteration(self):
        if self.has_reached_limit():
            return True
        if self.index < len(self.video_list):
            return False
        else:
            return not self.configure_video_list()


    def has_reached_limit(self):
        if not self.index < self.limit:
            return True
        else:
            return False


    def configure_timestamp(self):
        self.video_list[self.index]['timestamp'] = generate_timestamp(self.video_list[self.index]['time'])