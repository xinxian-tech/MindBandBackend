import wave
import numpy as np
from pypianoroll import Multitrack, Track
from pitch import freqToPitch, pitchToName

import matplotlib.pyplot as plt


class humming:
    def mode(self, array):
        counts = np.bincount(array)
        while True:
            ans = np.argmax(counts)
            if ans == 0:
                counts[ans] = 0
                if sum(counts) == 0:
                    return 0
            else:
                return ans

    def openWaveFile(self, file):
        with wave.open(file, 'rb') as f:
            self.numChannels = f.getnchannels()
            self.sampleWidth = f.getsampwidth()
            self.frameRate = f.getframerate()
            length = f.getnframes() // 256 * 256
            self.waveData = np.fromstring(f.readframes(length), dtype=np.int16)
            # print(self.waveData)
            f.close()

        self.waveData.shape = -1, self.numChannels
        self.waveData = self.waveData.T
        self.waveData = np.mean(self.waveData, 0)

    def __init__(self, waveFileName, sampleLength=0.01, sampleStepLength=0.01):
        self.openWaveFile(waveFileName)

        self.sampleStepLength = sampleStepLength
        sampleSize = int(self.frameRate * sampleLength)
        sampleStep = int(self.frameRate * sampleStepLength)
        meanVolume = sum(self.waveData ** 2) / len(self.waveData)

        self.humming = []
        tune = []
        silent = True

        print("ready")

        for time in range(0, len(self.waveData) - sampleSize, sampleStep):
            sample = self.waveData[time: time + sampleSize]

            volume = sum(sample ** 2) / len(sample)
            # print("volume: %.0f / %.0f" % (volume, meanVolume), volume > meanVolume / 2)
            if volume < meanVolume * 0.1:
                if not silent:
                    self.humming.append((self.mode(tune), len(tune)))
                    silent = True
                    tune = [0]
                else:
                    tune.append(0)
                continue
            elif silent:
                self.humming.append((self.mode(tune), len(tune)))
                silent = False
                tune = []

            try:
                ans = []
                acceptRange = 12
                step = int(sampleSize ** 0.5)
                ansStep = None
                for i in range(0, sampleSize, step):
                    sample_ = np.array(
                        self.waveData[time+i: time+sampleSize+i], dtype=np.float)
                    delta = sum((sample - sample_) ** 2) * (100 + i)
                    ans.append(delta)
                    if i > acceptRange * 2 + 1:
                        _acceptRange = acceptRange//step
                        if _acceptRange == 0:
                            _acceptRange = 1
                        test = ans[_acceptRange: -_acceptRange]
                        argmin = np.argmin(test)
                        if argmin != 0 and argmin != len(test) and argmin != len(test)-1:
                            # print("argmin =", argmin, "i =", i)
                            ansStep = (argmin + acceptRange//step) * step
                            # print(ansStep)
                            break
                ans = []
                for i in range(ansStep - step * 2, ansStep + step * 2):
                    sample_ = np.array(
                        self.waveData[time+i: time+sampleSize+i], dtype=np.float)
                    delta = sum((sample - sample_) ** 2)
                    ans.append(delta)
                    argmin = np.argmin(ans)
                    if argmin != 0 and argmin != len(ans) and argmin != len(ans)-1:
                        ans = ansStep - step * 2 + argmin
                        ans = 2 * self.frameRate / ans
                        break
                    # print('%d\t%f\n' % (i, delta))
                if isinstance(ans, list):
                    tune.append(0)
                else:
                    print(time / self.frameRate, int(ans),
                          freqToPitch(ans), sep='\t')
                    tune.append(freqToPitch(ans))
            except Exception:
                tune.append(0)

        else:
            if silent:
                self.humming.append((0, 0))
            else:
                self.humming.append((self.mode(tune), len(tune)))
                self.humming.append((0, 0))
        print(self.humming)

        def joinSilence(melody):
            ans = []
            for (p, l) in melody:
                if p == 0 and len(ans) != 0:
                    ans[-1] = (ans[-1][0], ans[-1][1] + l)
                if p != 0:
                    ans.append((p, l))
            return ans

        self.humming = joinSilence(self.humming)
        print(self.humming)

        def calcBeatResolution(melody):
            return 5
            ans, loss = None, 0
            minLength = min([item[1] for item in melody])
            for i in range(100):
                tempans = i * 1/self.sampleStepLength / 100
                length = tempans * self.sampleStepLength
                if tempans < minLength / 2:
                    continue
                temploss = 0
                for item in melody:
                    beat = item[1] / tempans
                    if beat < 0.5:
                        temploss += (1 / beat) ** 2
                    else:
                        temploss += (beat - round(beat)) ** 2
                temploss /= len(melody)
                if ans is None or loss > temploss:
                    ans, loss = tempans, temploss
                # print(tempans, i, temploss)
            return ans

        self.beatResolution = calcBeatResolution(self.humming)

        self.humming = [(item[0], round(item[1]/self.beatResolution))
                        for item in self.humming]

    def fillFullBar(self, bar=4):
        length = sum([b for (a, b) in self.humming])
        pad = (bar - length % bar) % bar
        a, b = self.humming[-1]
        self.humming[-1] = (a, b + pad)

    def filter(self, sampleSize=100):
        self.humming = filter(self.humming, sampleSize)

    def saveMidiFile(self, midiFileName, divider=16):
        print('saveMidiFile')
        length = sum(item[1] for item in self.humming)
        pianoRoll = np.zeros((length*divider, 128), dtype=np.int8)
        time = 0
        for (p, l) in self.humming:
            pianoRoll[time: time+l*divider-1, p] = 100
            time += l*divider
        track = Track(pianoroll=pianoRoll, program=0, name='')
        multitrack = Multitrack(
            tracks=[track],
            beat_resolution=2*divider,
            tempo=round(30/self.sampleStepLength/self.beatResolution))
        print("sampleStepLength :", self.sampleStepLength)
        print("beatResolution :", self.beatResolution)
        multitrack.write(midiFileName)


if __name__ == '__main__':
    h = humming('1.wav')
    h.fillFullBar()
    # print(h.humming)
    # h.filter(9)
    # h.filter(3)
    # print(h.humming)
    h.saveMidiFile(r'C:\Users\Administrator\Desktop\MindBandBackend\api\humming\1.mid')
