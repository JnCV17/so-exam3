from flask import Flask
import json
from status import Status

app = Flask(__name__)

@app.route('/v1/status/cpu')
def get_cpuinfo():
    cpu_percent = Status.get_cpu_percent()
    return json.dumps({'uso_de_cpu': cpu_percent})

@app.route('/v1/status/memory')
def get_memoryinfo():
    memory_info = Status.get_available_memory()
    return json.dumps({'memoria_disponible(MB)': memory_info})

@app.route('/v1/status/disk')
def get_diskinfo():
    disk_info = Status.get_disk_space()
    return json.dumps({'espacio_en_disco(MB)': disk_info})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
