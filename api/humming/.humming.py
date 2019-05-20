import wave
import numpy as np
from scipy import signal
from pypianoroll import Multitrack, Track
from pitch import freqToPitch, pitchToName
import matplotlib.pyplot as plt


# wave data
class wav():
    ignoreFrequencyMoreThan = 800

    def __init__(self, file):
        self.openWaveFile(file)

    # open a wave file and save wave data
    def openWaveFile(self, file):
        with wave.open(file, 'rb') as f:
            self.numChannels = f.getnchannels()
            self.sampleWidth = f.getsampwidth()
            self.frameRate = f.getframerate()
            length = f.getnframes() // 256 * 256
            self.data = np.frombuffer(f.readframes(length), dtype=np.int16)
            self.data = np.array(self.data, dtype=np.float)

        self.data.shape = -1, self.numChannels
        self.data = self.data.T
        self.data = np.mean(self.data, 0)
        return self

    # sample a wave file
    # return: iterable
    def sample(self, length=0.01, step=0.02):
        self.sampleLength = length
        self.sampleStep = step
        sampleSize = int(self.frameRate * length)
        sampleStep = int(self.frameRate * step)
        return [
            (i, i + sampleSize, i / self.frameRate)
            for i in range(0, len(self.data) - sampleSize, sampleStep)
        ]

    # return: [freq]
    def frequency(self, start, end):
        def search(sample, start, end, divide=150):
            start = max(start, 0)
            end = min(end, len(self.data))
            length = (end - start) // divide
            # print("search(%d, %d), length=%d" % (start, end, length))
            if length < 1:
                if end - start <= 2:
                    return (start + end) // 2
                else:
                    length = 1

            ans = []
            for i in range(start + length, end, length):
                try:
                    deltaSample = self.data[i: i+len(sample)]
                    delta = sum((sample - deltaSample) ** 2) * \
                        (i - start + self.frameRate /
                         self.ignoreFrequencyMoreThan) ** 0.5
                    ans.append((delta, i))
                    # print('delta(%d)=%f' % (i, delta))
                except Exception:
                    pass

            temp = None
            while ans:
                i = ans.index(min(ans))
                if i == 0 or i == len(ans) - 1:
                    if temp is None:
                        temp = ans[i]
                    ans.remove(ans[i])
                else:
                    time = ans[i][1]
                    return search(sample, time - length, time + length)
            else:
                time = temp[1]
                return search(sample, time - length, time + length)

        sample = self.data[start:end]
        startFrom = self.frameRate // self.ignoreFrequencyMoreThan
        searchTime = search(sample, start + startFrom, end)
        try:
            ignoreFrom = startFrom // 2
            deltaSample = self.data[searchTime: searchTime+end-start]
            delta0Sample = self.data[start+ignoreFrom: end+ignoreFrom]
            delta = sum((sample - deltaSample) ** 2)
            delta0 = sum((sample - delta0Sample) ** 2)
            if delta > delta0:
                return None
            raise Exception
        except Exception:
            return self.frameRate / (searchTime - start) * 2

    # return: [vol]
    def volume(self, start, end):
        def v(data): return sum(data ** 2) ** 0.5 / len(data)
        try:
            self.meanVolumn
        except:
            volumes = [
                v(self.data[start: end])
                for start, end, time in self.sample()
            ]
            self.meanVolumn = np.mean(volumes)
            self.stdVolumn = np.std(volumes)

        v = (v(self.data[start: end])) / self.stdVolumn
        return v

    def parse(self):
        return [
            (
                self.frequency(start, end),
                self.volume(start, end),
                time
            )
            for start, end, time in self.sample()
        ]

    def buffer(self, parsed, size=3):
        def mid(array):
            return sorted(array)[len(array)//2]

        ans = []
        for i in range(len(parsed)-size+1):
            frequencies = [parse[0] for parse in parsed[i:i+size]]
            volumes = [parse[1] for parse in parsed[i: i+size]]
            times = [parse[2] for parse in parsed[i: i+size]]

            volume = sum(volumes) / size
            if volume < -1 or not all([self.validFrequency(f) for f in frequencies]):
                frequency = None
            else:
                frequency = round(mid(frequencies), 3)
            time = sum(times) / size

            ans.append((frequency, volume, time))
        return ans

    def validFrequency(self, frequency):
        if frequency is None:
            return False
        return 0 < frequency < self.ignoreFrequencyMoreThan


class melody():
    # save melody in midi file
    def saveMidiFile(self, file):
        pass

    def calcPitch(self, parsed):
        def positionWeight(x):
            return x * (x-1) ** 2

        def accurancyWeight(f, mid):
            return ((freqToPitch(f)-freqToPitch(mid)) ** 8 + 1) ** -0.5

        length = len(parsed)
        parsed = list(filter(lambda x: x[0] is not None, parsed))
        if len(parsed) == 0:
            return (None, length)
        mid = sorted(parsed)[len(parsed) // 2][0]
        s = w = 0
        for i in range(len(parsed)):
            position = (i+0.5) / len(parsed)
            weight = positionWeight(position) * \
                accurancyWeight(parsed[i][0], mid)
            s += weight * parsed[i][0]
            w += weight
        return (freqToPitch(s / w, 0), length)

    # parse melody from parsed wav

    def fromWav(self, parsed):
        def volumeConfidence(parsed, x, before=5, after=5):
            v = parsed[x][1]
            confidence = (v if v < 0 else 0)
            for i in range(1, after+1):
                try:
                    # confidence += (parsed[x+i-1][1] / v - 1) / i
                    confidence += (v - parsed[x+i][1]) / i * 0.5
                except Exception:
                    pass
            for i in range(1, before+1):
                try:
                    confidence += (v - parsed[x-i][1]) / i * 1.5
                except Exception:
                    pass
            return confidence

        def frequencyConfidence(f, f0):
            if f is None or f0 is None:
                return 0.2
            delta = abs(freqToPitch(f, 0) - freqToPitch(f0, 0))
            if delta < 0.5:
                return 0
            elif delta < 1:
                return delta - 0.5
            else:
                return 0.5

        confidences = []
        for i in range(len(parsed)):
            confidence = 0
            if i == 0:  # or parsed[i][0] is None:
                confidence = 0
            else:
                confidence += volumeConfidence(parsed, i)
                confidence += frequencyConfidence(parsed[i][0], parsed[i-1][0])

            confidences.append(confidence)

        a = b = 0
        ans = []
        while b < len(confidences):
            if a >= b:
                b += 1
                continue
            if b-a > 5:
                a += 1
                continue
            c0 = sum(confidences[a:b]) / (b-a+1) * 2
            c = sum(confidences[a+1:b]) / (b-a) * 2
            if c > c0:
                a += 1
                continue
            if c0 > 1:
                ans.append((a + b) // 2)
                a = b + 3
            b += 1

        for i in range(len(parsed)):
            if i in ans:
                print('stress here')
            f, v, t = parsed[i]
            print(freqToPitch(f, 3), round(v, 3),
                  round(t, 2), confidences[i], sep='\t')

        ans.append(len(parsed))
        for i in range(len(ans)-1):
            print(self.calcPitch(parsed[ans[i]:ans[i+1]]))


if __name__ == '__main__':
    w = wav('1.wav')
    parsed = w.buffer(w.parse())
    m = melody()
    m.fromWav(parsed)
