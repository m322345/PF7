from typing import Optional
from fastapi import FastAPI
from pathlib import Path
import lightgbm as lgb
from lightgbm import LGBMClassifier
import pandas as pd
import pickle


def get_file_number(filename):
    f = open(filename)
    content = f.read()
    value = float(content)
    f.close()
    return value


app = FastAPI()
baseDir = str(Path(__file__).parent)
seuil = get_file_number(baseDir+"/Data/Seuil.txt")
model = pickle.load( open(baseDir+"/Data/Model/model.pkl", "rb" ) )
ClientsDatabase = pd.read_csv(baseDir+"/Data/Db/ClientDatabase.csv")


@app.get("/")
async def root():
    return " Bienvenue sur notre API "

@app.get("/request/{client_id}")
def return_pred(client_id: int):
    ClientsDatabaseList = list(ClientsDatabase['SK_ID_CURR'].unique())

    if client_id == 999: # Client test pour test unitaire
        return {"client_id": client_id, "risk": "risky", "status": "TestUser"}
    elif client_id not in ClientsDatabaseList: # Client inconnu de la base
        return {"error": "Client inconnu de notre base"}
    else:
        X = ClientsDatabase[ClientsDatabase['SK_ID_CURR'] == client_id]
        X = X.drop(['SK_ID_CURR','TARGET'], axis=1)
        risk = model.predict_proba(X)[:, 1][0]
        #tauxRisk = risk
        if risk > seuil:
            status = "Refusé"
        else:
            status = "Accordée"
        return {"client_id": client_id, "risk": risk, "status": status}