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
    

    soundRecord = sR.SoundRecordThread(INDEX=2, CHANNELS=1, RATE=48000, 
    DELAY_SECONDS=2)
    soundPlay = sP.SoundPlayThread(CHANNELS=1, DELAY_SECONDS=2, INDEX=11)

    soundRecord.start()
    soundPlay.start()

    get_sound_device()

    while True:
        sound = soundRecord.get_sound()
        if sound is not None:
            soundPlay.add_sound(sound)

        # get_sound_device()

    soundRecordThread.stop()
    soundPlayThread.stop()

main()