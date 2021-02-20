from twisted.internet import protocol
import queue
import msgpack
import msgpack_numpy
msgpack_numpy.patch()


# from Sound import soundPlayThread, soundRecordThread

# sudo apt-get install telnetd

class RaspberryPIProtocol(protocol.Protocol):

  def __init__(self, queueData, name):
    self.unpacker = msgpack.Unpacker()
    self.queueData = queueData
    self.name = name

    # self.soundRecord = soundRecordThread.SoundRecordThread(INDEX=1, CHANNELS=1, RATE=48000, 
    # DELAY_SECONDS=2, server=self.transport)
    # self.soundPlay = soundPlayThread.SoundPlayThread(CHANNELS=2)

    # self.soundRecord.start()
    # self.soundPlay.start()

  def connectionMade(self):
    print("Connect")

    hello = {
      "type": "client_connect",
      "data": self.name
    }

    self.send_message(hello)

  def send_message(self, data):
    if self.transport is not None:
      msgpack.pack(data, self.transport)
    
  def dataReceived(self, data):
    self.unpacker.feed(data)
    for msg in self.unpacker:
      # if msg["type"] == "soundsPC":
      #   sound_pc = msg["data"]
      #   if sound_pc is not None:
      #     # print(sound_pc)
      #     self.soundPlay.add_sound(sound_pc)
      self.add_data(msg["type"], msg["data"])
    
  def connectionLost(self, reason):
    print("connection lost")

  def add_data(self, name, data):
    try:
      self.queueData[name].put_nowait(data)
    except queue.Full:
      pass
