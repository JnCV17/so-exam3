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
