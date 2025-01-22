# Test unitaire
import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient
import pytest
from Api.main import get_file_number, app

#sys.path.append(os.path.abspath('../Api'))
client = TestClient(app)

# Test pour tester la récupération du seuil fourni a l'api
def test_recupSeuil():
    get_file_number(str(Path(__file__).parent)+"/Seuil.txt") == 314116
 
# Test de l'accès à la racine de l'api
def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ' Bienvenue sur notre API '

# Test de réponse si client est connu de la base
def test_api_clientConnu():
    response = client.get("/request/999")
    assert response.status_code == 200
    assert response.json() == {"client_id": 999, "risk": "risky", "status": "TestUser"}

# Test de réponse si client inconnu de la base
def test_api_clientInconnu():
    response = client.get("/request/007")
    assert response.status_code == 200
    assert response.json() == {"error": "Client inconnu de notre base"}
    
