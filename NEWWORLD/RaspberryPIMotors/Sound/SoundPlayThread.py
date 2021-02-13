import threading
import queue
import pyaudio

class SoundPlayThread(threading.Thread):
    def __init__(self, CHUNK = 1024, CHANNELS = 1, RATE = 44100, DELAY_SECONDS = 5, INDEX = 7):
        super().__init__()

        self._stopped       = False

        self.CHUNK          = CHUNK
        self.CHANNELS       = CHANNELS
        self.RATE           = RATE
        self.INDEX          = INDEX
        self.DELAY_SECONDS  = DELAY_SECONDS
        self.DELAY_SIZE     = int(self.DELAY_SECONDS * self.RATE / (10 * self.CHUNK))

        self.FORMAT         = pyaudio.paInt16
        self.p              = pyaudio.PyAudio()

        self.queue_sound    = queue.Queue(self.DELAY_SIZE)

        self.stream         = None

    def run(self):
        self.init_audio()
        while not self._stopped:
            try:
                sound = self.queue_sound.get_nowait()
                if sound is not None:
                    for i in range(len(sound)):
                        self.stream.write(sound[i])
            except queue.Empty:
                pass

    def init_audio(self):
        self.stream = self.p.open(
            format              =self.FORMAT,
            channels            =self.CHANNELS,
            rate                =self.RATE,
            output               =True,
            frames_per_buffer   =self.CHUNK,
            output_device_index  = self.INDEX)

    def add_sound(self, frame):
        try:
            return self.queue_sound.put(frame)
        except queue.Full:
            pass
    
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        self._stopped = True
