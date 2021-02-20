import threading
import queue
import pyaudio
import cv2
import time

class SoundRecordThread(threading.Thread):
    def __init__(self, CHUNK = 1024, CHANNELS = None, RATE = None, DELAY_SECONDS = 5, INDEX = None, server=None):
        super().__init__()

        self._stopped       = False
        self.server = server

        self.CHUNK          = CHUNK
        self.CHANNELS       = CHANNELS
        self.RATE           = RATE
        self.INDEX          = INDEX
        self.DELAY_SECONDS  = DELAY_SECONDS

        self.FORMAT         = pyaudio.paInt16
        self.p              = pyaudio.PyAudio()
        self.default_device = self.p.get_default_input_device_info()

        self.stream         = None

        if CHANNELS is None:
            self.CHANNELS   = self.default_device["maxInputChannels"]

        if RATE is None:
            self.RATE       = int(self.default_device["defaultSampleRate"])

        if INDEX is None:
            self.INDEX      = self.default_device["index"]

        self.DELAY_SIZE     = int(self.DELAY_SECONDS * self.RATE / (10 * self.CHUNK))
        self.queue_sound    = queue.Queue(self.DELAY_SIZE)

        # self.cam = cv2.VideoCapture(1)

    def run(self):
        self.init_audio()
        while not self._stopped:
            # ret, frames = self.cam.read()
            # cv2.waitKey(1)
            frame = []
            for i in range(10):
                frame.append(self.stream.read(self.CHUNK,exception_on_overflow = False))
            
            try:
                # print(sound)
                # print(frame)
                # self.server.send_message({
                #     "type": "soundsRaspberry", 
                #     "data": frame
                # })
                # pass
                self.queue_sound.put(frame)
            except queue.Full:
                pass

    def init_audio(self):
        self.stream = self.p.open(
            format              = self.FORMAT,
            channels            = self.CHANNELS,
            rate                = self.RATE,
            input               = True,
            frames_per_buffer   = self.CHUNK,
            input_device_index  = self.INDEX
        )

    def get_sound(self):
        try:
            return self.queue_sound.get_nowait()
        except queue.Empty:
            return None
    
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        self._stopped = True
