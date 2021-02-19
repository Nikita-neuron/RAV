import multiprocessing as mp
import pyaudio
import wave

import SoundRecordThread as sR
import SoundPlayThread as sP

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
            print("Input Device id ", i, " - ", 
            p.get_device_info_by_host_api_device_index(0, i).get('name'), " chanels: ", 
            p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels'), 
            "RATE: ", p.get_device_info_by_host_api_device_index(0, i).get('defaultSampleRate'))

    print("-------------------------------------------------------------")
    p.terminate()

def main():
    get_sound_device()

    soundRecordThread = sR.SoundRecordThread(INDEX=1, CHANNELS=1, RATE=44100)
    soundPlayThread = sP.SoundPlayThread(INDEX=5, CHANNELS=1, RATE=44100)

    soundRecordThread.start()
    soundPlayThread.start()

    while True:
        sound = soundRecordThread.get_sound()
        if sound is not None:
            soundPlayThread.add_sound(sound)

    soundRecordThread.stop()
    soundPlayThread.stop()

main()