import pytest
from application.app import app
from flask import Flask
import os


# Skapar en pytest-miljö som för att testen ska kunna köras.
@pytest.fixture()
def client():
    # Sätter igång appens testläge.
    app.config['TESTING'] = True
    # Skapar en klient för att göra webbanrop.
    client = app.test_client()
    # Returnerar klienten som en fixture för tester att använda.
    yield client


# Kontrollerar om startsidan returnerar statuskod 200.
def test_startsida(client):
    response = client.get('/')
    assert response.status_code == 200


# Kontrollerar att /elpriser, returnerar HTTP-statuskoden 200.
def test_elpriser(client):
    response = client.get('/elpriser')
    assert response.status_code == 200


# kontrollerar om POST-förfrågan görs till /elpriser att det returnerar HTTP-statuskoden 200.
def test_elpriser_post(client):
    response = client.post('/elpriser', data={'selectedDate': '2023-11-06', 'PRISKLASS': 'SE2'})
    assert response.status_code == 200


# kontrollerar om POST-förfrågan till /elpriser med ogiltig som 404
def test_elpriser_post_invalid_data(client):
    response = client.post('/elpriser', data={'selectedDate': 'invalid-date', 'PRISKLASS': 'invalid-price'})
    assert response.status_code == 404


# Kontrollerar om en specifik felkodssida, /felkod, returnerar statuskod 404
def test_felkod(client):
    response = client.get('/felkod')
    assert response.status_code == 404


# Kontrollerar om en sida som inte finns, returnerar statuskod 404
def test_404(client):
    response = client.get('/404')
    assert response.status_code == 404

