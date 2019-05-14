import json
import random

with open('api/va.json') as f:
    vajson = json.load(f)

db = [[[] for _ in range(10)] for _ in range(10)]

for songid in vajson:
    va = vajson[songid]
    db[int(va[0]+0.5)][int(va[1]+0.5)].append(songid)


def va2mp3(v, a, d=0):
    songs = []

    while len(songs) <= 20:
        for i in range(v - d, v + d + 1):
            if not 1 <= i <= 9:
                continue

            for j in range(a - d, a + d + 1):
                if not 1 <= j <= 9:
                    continue

                songs += db[i][j]

        d += 1

    return songs[random.randint(0, len(songs) - 1)]
