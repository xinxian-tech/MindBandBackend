emoji = {
    0x1F620: (2.3, 6.1),
    0x1F616: (2.7, 5.8),
    0x1F615: (3.8, 3.5),
    0x1F622: (2.6, 4.2),
    0x1F61E: (2.8, 3.2),
    0x1F611: (4.8, 3.8),
    0x1F631: (4.2, 6.6),
    0x1F618: (8.1, 6.5),
    0x1F613: (2.8, 4.1),
    0x1F61B: (7.6, 6.3),
    0x1F61D: (6.7, 6.4),
    0x1F61C: (7.6, 6.7),
    0x1F602: (7.1, 6.8),
    0x1F633: (5.1, 5.7),
    0x1F62C: (4.4, 5.8),
    0x1F600: (8.4, 6.7),
    0x1F601: (5.5, 5.9),
    0x1F62D: (3.1, 5.6),
    0x1F610: (5.0, 3.9),
    0x1F614: (3.4, 3.1),
    0x1F623: (3.1, 4.8),
    0x1F60C: (7.2, 3.5),
    0x1F634: (5.7, 2.3),
    0x263A: (7.6, 5.2),
    0x1F60D: (8.5, 7.1),
    0x1F60A: (7.9, 5.5),
    0x1F604: (8.2, 6.6),
    0x1F60E: (7.7, 5.0),
    0x1F60F: (6.1, 4.7),
    0x1F62B: (2.6, 5.6),
    0x1F612: (3.6, 3.7),
    0x1F629: (2.5, 5.2),
    0x1F609: (7.5, 5.4),
}


def emoji2VA(character):
    try:
        return emoji[ord(character)]
    except Exception as e:
        print(e)
        return None
