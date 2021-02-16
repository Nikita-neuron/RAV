import multiprocessing as mp
import pyaudio

import Sound.soundRecordThread as sR
import Sound.soundPlayThread as sP

def get_sound_device():
    p = pyaudio.PyAudio()
    print("----------------------default record device list---------------------")
    print(p.get_default_input_device_info())
    print(p.get_default_output_device_info())
    print("---------------------------------------------------------------------")
    print("----------------------record device list---------------------")
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'), " chanels: ", p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels'))

    print("-------------------------------------------------------------")
    p.terminate()


get_sound_device()

soundRecordThread = sR.SoundRecordThread()
soundPlayThread = sP.SoundPlayThread()

soundRecordThread.start()
soundPlayThread.start()

while True:
    sound = soundRecordThread.get_sound()
    soundPlayThread.add_sound(sound)

soundRecordThread.stop()
soundPlayThread.stop()
