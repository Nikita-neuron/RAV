from twisted.internet import protocol
import queue
import msgpack
import msgpack_numpy
msgpack_numpy.patch()


class PCMotorsProtocol(protocol.Protocol):
  def __init__(self):
    self.video_frames       = queue.Queue(2)
    self.sounds_raspberry   = queue.Queue(2)
    self.system_data        = queue.Queue(2)

    self.unpacker = msgpack.Unpacker()

    self.queueData = {
      "frames":           queue.Queue(2),
      "soundsRaspberry":  queue.Queue(2),
      "systemData":       queue.Queue(2)
    }

  def connectionMade(self):
    print("Connect")
    # self.transport.write(b"Hello")
    
  def dataReceived(self, data):
    # получение сообщений от распберри
    print("kkkk")
    self.unpacker.feed(data)
    for msg in self.unpacker:
      # print(msg)
      # if msg[0] == "frames":
        # print("o")
      print("data recv")
      self.add_data(msg[0], msg[1])
      print("done")
    # print("from raspberry: ", data)

    # if data[0] == "video":
    #   self.add_video_frames(data[1])
    # elif data[0] == "system":
    #   self.add_system_data(data[1])
    # elif data[0] == "sound":
    #   self.add_sound_raspberry(data[1])

    # self.add_data(data[0], data[1])

  def sendMessage(self, data):
    # отправка сообщений на распберри
    if self.transport is not None:
      print("sending")
      msgpack.pack(data, self.transport)
      print("done")

  def add_data(self, name, data):
    try:
      self.queueData[name].put(data, block=False)
    except queue.Full:
      pass

  def get_data(self, name):
    try:
      return self.queueData[name].get_nowait()
    except queue.Empty:
      return None
  '''
  def add_video_frames(self, frame):
    # добавление кадров в очередь
    try:
      self.video_frames.put(frame, block=False)
    except queue.Full:
      pass

  def get_video_frames(self):
    # получение кадров из очереди
    try:
      frame = self.video_frames.get_nowait()
      return frame
    except queue.Empty:
      return None

  def add_system_data(self, system_data):
    # добавление системных данных в очередь
    try:
      self.system_data.put(system_data)
    except queue.Full:
      pass

  def get_sys_data(self):
    # получение системных данных из очереди
    try:
      return self.system_data.get_nowait()
    except queue.Empty:
      return None

  def get_sound_raspberry(self):
    # получение звука из очереди
    try:
      return self.sounds_raspberry.get_nowait()
    except:
      return None

  def add_sound_raspberry(self, sound):
    # добавление звука в очередь
    try:
      self.sounds_raspberry.put(sound)
    except queue.Full:
      pass
  '''
  def print(self, data):
    print("")
    print("[RASPBERRY PI MOTORS]: ", data)
