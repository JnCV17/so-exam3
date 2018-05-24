import psutil

class Status():

  @classmethod
  def get_cpu_percent(cls):
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

  @classmethod
  def get_available_memory(cls):
    available_memory = psutil.virtual_memory().available >> 20
    return available_memory

  @classmethod
  def get_disk_space(cls):
    disk_space = psutil.disk_usage('/').free >> 20
    return disk_space
