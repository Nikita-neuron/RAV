import psutil
from gpiozero import CPUTemperature

class SystemData:
  def __init__(self):
    pass

  def cpu(self):
    return psutil.cpu_percent()

  def memory(self):
    memory = psutil.virtual_memory()
    # Divide from Bytes -> KB -> MB
    available = round(memory.available/1024.0/1024.0,1)
    total = round(memory.total/1024.0/1024.0,1)

    # all data in Bytes

    return {
      "memoryFree": available,
      "memoryTotal": total,
      "memoryPercent": memory.percent
    }

  def disk(self):
    disk = psutil.disk_usage('/')
    # all data in Bytes
    
    # Divide from Bytes -> KB -> MB
    free = round(disk.free/1024.0/1024.0,1)
    total = round(disk.total/1024.0/1024.0,1)
    # return str(free) + 'GB free / ' + str(total) + 'GB total ( ' + str(disk.percent) + '% )
    return {
      "diskFree": free,
      "diskTotal": total,
      "diskPercent": disk.percent
    }

  def temperature(self):
    cpu = CPUTemperature()
    return cpu.temperature

  def get_system_data(self):
    cpuData = self.cpu()
    memoryData = self.memory()
    diskData = self.disk()
    temperatureData = self.temperature()

    return {
        "cpu": cpuData,
        "memory": memoryData,
        "disk": diskData,
        "temperature": temperatureData
    }