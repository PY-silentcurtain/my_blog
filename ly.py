import threading
import pyaudio
import wave

class RecordThread(threading.Thread):
    def __init__(self, audiofile='record.wav'):
        threading.Thread.__init__(self)
        self.bRecord = True
        self.audiofile = audiofile
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1 #单通道
        self.rate = 32000 #采样率为32000

    def run(self):
        audio = pyaudio.PyAudio()
        wavfile = wave.open(self.audiofile, 'wb')#打开文件，用二进制写模式
        wavfile.setnchannels(self.channels)
        wavfile.setsampwidth(audio.get_sample_size(self.format))
        wavfile.setframerate(self.rate)
        wavstream = audio.open(format=self.format, 
                               channels=self.channels,
                               rate=self.rate,
                               input=True,
                               frames_per_buffer=self.chunk)
        while self.bRecord:
            wavfile.writeframes(wavstream.read(self.chunk))
         
        #停止数据流
        wavstream.stop_stream()#文件写完之后跳出
        wavstream.close()#不要忘记关闭文件哦
        audio.terminate()#到这里就终止啦

    def stoprecord(self):
        self.bRecord = False

if __name__ == "__main__":
    li = ['滑稽', '研究所', ]
    for i in li:
        file_name = i + '.wav'
        audio_record = RecordThread(file_name)
        audio_record.start()#开始录音
        key = input("请按回车键结束录音,朗读___________" + i + "___________")
        audio_record.stoprecord()#停止录音，调用参数变成False结束循环