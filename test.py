import vlive


def main():
    channel_seq = 128 #GFRIEND:128, Red Velvet:548
    [print('%s, %s, %s, %s'%(i['video_seq'], i['time'], i['timestamp'], i['title'])) for i in vlive.channel(channel_seq)]
    video_list = vlive.channel(548)
    print(vlive.embed_code(video_list.video_list[0]['video_seq']))


if __name__ == '__main__':
    main()