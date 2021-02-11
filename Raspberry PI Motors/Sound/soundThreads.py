import multiprocessing as mp
import pyaudio

import SoundRecordThread
import SoundPlayThread

CHUNK = 1024
CHANNELS = 1
RATE = 44100
DELAY_SECONDS = 5
DELAY_SIZE = DELAY_SECONDS * RATE / (10 * CHUNK)

def get_sound_device():
    p = pyaudio.PyAudio()
    print("----------------------record device list---------------------")
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'), " chanels: ", p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels'))

    print("-------------------------------------------------------------")
    p.terminate()


get_sound_device()

# print(pyaudio.PyAudio().is_format_supported(input_format=pyaudio.paInt16, input_channels=CHANNELS, rate=RATE, input_device=1))

soundRecordThread = SoundRecordThread.SoundRecordThread()
soundPlayThread = SoundPlayThread.SoundPlayThread()

soundRecordThread.start()
soundPlayThread.start()

while True:
    sound = soundRecordThread.get_sound()
    soundPlayThread.add_sound(sound)

soundRecordThread.stop()
soundPlayThread.stop()
