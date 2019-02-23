import vlive


def main():
    channel_seq = 548 #GFRIEND:128, Red Velvet:548
    [print('%s, %s, %s, %s, %s'%(i['video_seq'], i['time'], i['timestamp'], i['channel'], i['title'])) for i in vlive.channel(channel_seq, allow_other_channel=False, allow_mini_replay=False)]
    [print(vlive.embed_code(i['video_seq'])) for i in vlive.channel(128) if '여자친구, 어디 감수광?!' in i['title']]


if __name__ == '__main__':
    main()