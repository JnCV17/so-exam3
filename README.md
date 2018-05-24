# so-exam3

**Universidad ICESI**  
**Curso:** Sistemas Operativos  
**Estudiante:** Juan Camilo Villada  
**Codigo:** A00320192  

## Actividad 3

Se inicia en la maquina virtual CentOS un nuevo ambiente con nombre flask_environment

```
$ mkvirtualenv flask_environment
$ workon flask_environment
```

Una vez dentro de este ambiente, se instalan los paquetes Flask y psutil por medio de

```
$ pip install Flask
```

```
$ pip install psutil
```

Una vez se instalan, se pueden almacenar las librerias instaladas con sus versiones correspondientes en un archivo de texto plano llamado requirements.txt

```
pip freeze > requirements.txt
```

Clonamos el repositorio so-exam3. Una vez finaliza la clonación, accedemos a so-exam3 y alli creamos un archivo python que llamaremos status.py

```
$ vim status.py
```

Este archivo contendra una clase con unos metodos encargados de realizar las consultas de información del sistema (consumo CPU, memoria disponible, espacio de disco duro disponible).

```
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
```

Tambien creamos un archivo que llamaremos app.py el cual sera el encargado de exponer los servicios del servicio web Flask, haciendo uso de status.py para obtener el consumo de cpu, la memoria disponible y el espacio de disco disponible.

```
$ vim app.py
```

```
from flask import Flask
import json

from status import Status

app = Flask(__name__)

@app.route('/v1/status/cpu')
def get_cpuinfo():
    cpu_percent = Stats.get_cpu_percent()
    return json.dumps({'uso_de_cpu': cpu_percent})

@app.route('/v1/status/memory')
def get_memoryinfo():
    memory_info = Stats.get_available_memory()
    return json.dumps({'memoria_disponible(MB)': memory_info})

@app.route('/v1/status/disk')
def get_diskinfo():
    disk_info = Stats.get_disk_space()
    return json.dumps({'espacio_en_disco(MB)': disk_info})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
```

Finalmente ejecutamos la aplicacion con el siguiente comando

```
python app.py
```

En caso de que las peticiones al servidor no devuelvan respuesta, hay que recordar habilitar el puerto a traves del firewall con el siguiente comando

```
firewall-cmd --zone=public --add-port=port-goes-here/tcp --permanent
```

y reiniciar el firewall para que los cambios tengan efecto

```
firewall-cmd --reload
```
