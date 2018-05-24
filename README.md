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
```

Finalmente ejecutamos la aplicacion con el siguiente comando

```
python app.py
```

![alt text](https://raw.githubusercontent.com/JnCV17/so-exam3/A00320192/imagenes/runningApp.png)

**Consulta Uso de CPU**

![alt text](https://raw.githubusercontent.com/JnCV17/so-exam3/A00320192/imagenes/status-cpu.png)

**Consulta Memoria disponible**

![alt text](https://raw.githubusercontent.com/JnCV17/so-exam3/A00320192/imagenes/status-memory.png)

**Consulta espacio en disco disponible**

![alt text](https://raw.githubusercontent.com/JnCV17/so-exam3/A00320192/imagenes/status-disk.png)

**Nota:**

En caso de que las peticiones al servidor no devuelvan respuesta, hay que recordar habilitar el puerto a traves del firewall con el siguiente comando

```
firewall-cmd --zone=public --add-port=port-goes-here/tcp --permanent
```

y reiniciar el firewall para que los cambios tengan efecto

```
firewall-cmd --reload
```

## Actividad 4

Una vez los servicios se han creado, es necesario realizar pruebas para verificar su estado, por lo tanto se implementaran pruebas para los servicios empleando Fixtures y Mocks.

Primero instalamos los componentes necesarios para realizar las pruebas, en este caso instalaremos pytest, mock y pytest_mock

```
pip install pytest
```

```
pip install mock
```

```
pip install pytest_mock
```

A continuación  se crea un archivo llamado test_status el cual contendra las pruebas unitarias para el servicio web

```
vim test_status.py
```

```
import pytest
import mock

from pytest_mock import mocker
from app import app
from status import Status

@pytest.fixture
def client():
  client = app.test_client()
  return client

def test_get_cpu_percent(mocker, client):
  mocker.patch.object(Status, 'get_cpu_percent', return_value=100)
  response = client.get('/v1/status/cpu')
  assert response.data.decode('utf-8') == '{"uso_de_cpu": 100}'
  assert response.status_code == 200

def test_get_available_memory(mocker, client):
  mocker.patch.object(Status, 'get_available_memory', return_value=2000)
  response = client.get('/v1/status/memory')
  assert response.data.decode('utf-8') == '{"memoria_disponible(MB)": 2000}'
  assert response.status_code == 200


def test_get_disk_space(mocker, client):
  mocker.patch.object(Status, 'get_disk_space', return_value=1000)
  response = client.get('/v1/status/disk')
  assert response.data.decode('utf-8') == '{"espacio_en_disco(MB)": 1000}'
  assert response.status_code == 200
```

Finalmente, ejecutamos las pruebas con el siguiente comando

```
pytest -v
```

![alt text](https://raw.githubusercontent.com/JnCV17/so-exam3/A00320192/imagenes/pytest.png)


## Actividad 5

En este punto se empleara un servicio de integracíon continua que hace uso de las pruebas unitarias desarrolladas para validar los commits a un servicio en linea usando TOX.

Primero instalaremos tox usando el siguiente comando

```
pip install tox
```

Una vez instalado tox, se creara un archivo tox.ini el cual contendra las especificaciones de: libreria para pruebas, lenguaje base (Python3, en este caso) y dependencias que se van a usar.

```
vim tox.ini
```

```
[tox]
envlist = py27, py34
skipsdist = true

[testenv]
commands = pytest
deps =
    mock
    pytest
    pytest_mock
    flask
    psutil
```

Y ejecutamos las pruebas con el comando **tox**

![alt text](https://raw.githubusercontent.com/JnCV17/so-exam3/A00320192/imagenes/tox.png)

Finalmente, para ejecutar las pruebas de commits, se usaran las pruebas de travis-ci.org, por lo tanto se creara un archivo .travis.yml donde se guardara la configuracion basica para correr las pruebas.

```
vim .travis.yml
```

```
sudo: false
language: python
notifications:
  email: false
python:
- '3.4'
install: pip install tox-travis
script: tox
```


