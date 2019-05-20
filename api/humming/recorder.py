import pyaudio
import wave


class recorder:
    def __init__(self, numChannels=2, sampleWidth=2, frameRate=44100, numSamples=4410):
        self.numChannels = numChannels
        self.sampleWidth = sampleWidth
        self.frameRate = frameRate
        self.numSamples = numSamples

    def saveWaveFile(self, waveFileName, data):
        with wave.open(waveFileName, 'wb') as f:
            f.setnchannels(self.numChannels)
            f.setsampwidth(self.sampleWidth)
            f.setframerate(self.frameRate)
            f.writeframes(data)
            f.close()

    def record(self, waveFileName, length):
        pa = pyaudio.PyAudio()
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=self.numChannels,
            rate=self.frameRate,
            input=True,
            frames_per_buffer=self.numSamples)
        buf = b''
        while length > len(buf) / self.frameRate / self.numChannels / self.sampleWidth:
            buf += stream.read(self.numSamples)
        stream.close()
        self.saveWaveFile(waveFileName, buf)


if __name__ == '__main__':
    r = recorder()
    r.record('1.m4a', 5)
