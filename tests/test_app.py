import pytest
from application.app import app
from flask import Flask
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_startsida(client):
    response = client.get('/')
    assert response.status_code == 200

def test_elpriser_get(client):
    response = client.get('/elpriser')
    assert response.status_code == 200


def test_elpriser_post(client):
    response = client.post('/elpriser', data={'selectedDate': '2023-11-06', 'PRISKLASS': 'SE2'})
    assert response.status_code == 200

def test_elpriser_post_invalid_data(client):
    response = client.post('/elpriser', data={'selectedDate': 'invalid-date', 'PRISKLASS': 'invalid-price'})
    assert response.status_code == 404

def test_felkod(client):
    response = client.get('/felkod')
    assert response.status_code == 404

def test_404(client):
    response = client.get('/404')
    assert response.status_code == 404

def test_elpriser_post_invalid_data(client):
    response = client.post('/elpriser', data={'selectedDate': 'invalid-date', 'PRISKLASS': 'invalid-price'})
    assert response.status_code == 404
