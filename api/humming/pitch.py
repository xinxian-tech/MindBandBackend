import math

names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
center = 60
mean = 440 * 2 ** 0.25


def pitchToFreq(pitch):
    pitch -= center
    freq = mean * pow(2, pitch / 12)
    return freq


def freqToPitch(freq, ndigits=None):
    if freq is None or freq <= 0:
        return 0
    pitch = math.log(freq/mean) / math.log(2) * 12 + center
    if ndigits is None:
        return int(pitch + 0.5)
    elif ndigits == 0:
        return pitch
    else:
        return round(pitch, ndigits)


def pitchToName(pitch):
    pitch = pitch - center + 36
    return names[pitch % 12] + str(pitch // 12)


if __name__ == '__main__':
    while True:
        freq = int(input())
        pitch = freqToPitch(freq)
        name = pitchToName(pitch)
        print(name)
