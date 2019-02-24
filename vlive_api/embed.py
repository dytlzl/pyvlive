class embed():
    EMBED_CODE = '<iframe src=https://www.vlive.tv/embed/%s?autoPlay=false" frameborder="no" scrolling="no" marginwidth="0" marginheight="0" WIDTH="544" HEIGHT="306" allowfullscreen></iframe>'


    def __new__(cls, video_seq):
        return cls.EMBED_CODE%(video_seq)