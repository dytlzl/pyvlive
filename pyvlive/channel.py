import requests
from .video import Video


class Channel:
    VLIVE_URI = 'https://api-vfan.vlive.tv/vproxy/channelplus/getChannelVideoList'
    VFAN_APP_ID = '8c6cc7b45d2568fb668be6e05b6e5a3b'
    MAX_NUM_LIST = 100

    def __init__(self, channel_seq, limit=1024, allow_other_channel=True, allow_mini_replay=True, search_word=''):
        self.channel_name = ''
        self.videos = []
        self.limit = limit
        self.is_allowed_other_channel = allow_other_channel
        self.is_allowed_mini_replay = allow_mini_replay
        self.search_word = search_word
        self.index = 0
        self.params = {
            'app_id': self.VFAN_APP_ID,
            'channelSeq': channel_seq,
            'maxNumOfRows': self.MAX_NUM_LIST,
            'pageNo': 1,
        }

    def __iter__(self):
        self.register_video_data()
        return self

    def __next__(self):
        if self.index >= self.limit or (self.index >= len(self.videos) and not self.register_video_data()):
            raise StopIteration
        try:
            self.videos[self.index].generate_timestamp()
            video = self.videos[self.index]
            self.index += 1
            return video
        except IndexError:
            return self.__next__()

    def fetch_video_list(self):
        res = requests.get(self.VLIVE_URI, params=self.params)
        data = res.json()
        return data

    def register_video_data(self):
        data = self.fetch_video_list()['result']
        self.channel_name = data['channelInfo']['channelName']
        try:
            for video_data in data['videoList']:
                if video_data['videoType'] != 'VOD'\
                        or (self.search_word != '' and self.search_word not in video_data['title'])\
                        or (not self.is_allowed_mini_replay and '[CH+ mini replay]' in video_data['title'])\
                        or (not self.is_allowed_other_channel and self.channel_name != video_data['representChannelName']):
                    continue
                self.videos.append(
                    Video(
                        video_data['videoSeq'],
                        video_data['title'],
                        video_data['representChannelName'],
                        video_data['onAirStartAt'],
                        video_data['playTime'],
                        video_data['thumbnail']
                    )
                )
        except KeyError:
            return False
        self.params['pageNo'] += 1
        return True
