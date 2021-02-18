import threading
import queue
import pyaudio
import wave

class SoundPlayThread(threading.Thread):
    def __init__(self, CHUNK = 1024, CHANNELS = None, RATE = None, DELAY_SECONDS = 5, INDEX = None):
        super().__init__()

        self._stopped       = False

        self.CHUNK          = CHUNK
        self.CHANNELS       = CHANNELS
        self.RATE           = RATE
        self.INDEX          = INDEX
        self.DELAY_SECONDS  = DELAY_SECONDS

        self.FORMAT         = pyaudio.paInt16
        self.p              = pyaudio.PyAudio()
        self.default_device = self.p.get_default_output_device_info()

        self.stream         = None

        if CHANNELS is None:
            self.CHANNELS   = self.default_device["maxOutputChannels"]

        if RATE is None:
            self.RATE       = int(self.default_device["defaultSampleRate"])

        if INDEX is None:
            self.INDEX      = self.default_device["index"]

        self.DELAY_SIZE     = int(self.DELAY_SECONDS * self.RATE / (10 * self.CHUNK))
        self.queue_sound    = queue.Queue(self.DELAY_SIZE)

    def run(self):
        self.init_audio()
        
        while not self._stopped:
            sound = None
            try:
                sound = self.queue_sound.get_nowait()
            except queue.Empty:
                pass
            if sound is not None:
                for i in range(len(sound)):
                    self.stream.write(sound[i])

    def init_audio(self):
        self.stream = self.p.open(
            format              = self.FORMAT,
            channels            = self.CHANNELS,
            rate                = self.RATE,
            output              = True,
            frames_per_buffer   = self.CHUNK,
            output_device_index = self.INDEX)

    def add_sound(self, frame):
        try:
            self.queue_sound.put_nowait(frame)
        except queue.Full:
            pass
    
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        self._stopped = True
