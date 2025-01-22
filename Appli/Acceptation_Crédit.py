import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt
import requests
import shap
import lightgbm
from pathlib import Path
import pickle


def get_file_number(filename):
    """recuperation du seuil etabli lors de l'elaboration du modele"""
    f = open(filename)
    content = f.read()
    value = float(content)
    f.close()
    return value


def request_prediction(model_uri, data):
    """interrogation de l'api"""
    headers = {"Content-Type": "application/json"}
    data_json = {'data': data}
    response = requests.request(method='GET', headers=headers, url=model_uri+'request/'+data)
    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(response.status_code, response.text))
    return response.json()


def visualize_importance(modele, id, donnees):
    """calcule la feature importance du modele"""
    X = DropColumns(donnees)
    prediction = lambda x: modele.predict_proba(x)[:, 1]
    moyennes = X.mean().values.reshape((1, X.shape[1]))
    explainer = shap.Explainer(prediction, moyennes)
    shap_values_single = explainer(Client(id,donnees), max_evals=1500)
    shap_values = explainer(X, max_evals=1500)
    return shap_values_single, shap_values


def DropColumns(dataset):
    """enleve """
    if 'SK_ID_CURR' in dataset.columns:
        dataset = dataset.drop(['SK_ID_CURR'], axis=1)
    if 'TARGET' in dataset.columns:
        dataset = dataset.drop(['TARGET'], axis=1)
    return dataset


def loadModel(modelPath):
    """retourne le modèle"""
    return pickle.load( open(modelPath, "rb" ) )


def Client(id,dataset):
    """retourne les informations du client"""
    return DropColumns(dataset.loc[dataset.SK_ID_CURR == id])


def set_state(i):
    """sauvegarde l'etat de la session"""
    st.session_state.etat = i


def main():
    #Url Api
    MODEL_URI = 'https://ocp7-api.onrender.com/'
    #fichier données
    pathDb = str(Path(__file__).parent)+'/../Api/Data/Db/'
    FichierSeuil = str(Path(__file__).parent)+'/../Api/Data/Seuil.txt'
    pathMod = str(Path(__file__).parent)+'/../Api/Data/Model/'
    ClientsDatabase = pd.read_csv(pathDb+'ClientDatabase.csv')
    ClientsList = ClientsDatabase['SK_ID_CURR'].tolist()
    Seuil = get_file_number(FichierSeuil)
    CouleurRefus = "#FF0051"
    CouleurAccord = "#008BFB"
    #creation de la session
    if 'etat' not in st.session_state:
        st.session_state.etat = 0
    #Menu
    user_id = st.sidebar.selectbox('Recherche client',ClientsList)
    predict_btn = st.sidebar.button('Calcul du risque', on_click=set_state, args=[user_id])
    st.sidebar.divider()
    st.sidebar.page_link("https://www.ewd.fr/Formation/Data/P7/Drift_du_Modèle.html", label='Visualisation Data Drift')
    #Page
    style_heading = 'text-align: center'
    st.markdown(f"<h1 style='{style_heading}'>Risque de faillite d\'un client</h1>", unsafe_allow_html=True)

    if st.session_state.etat != 0:
        with st.spinner("Merci de patienter, nous récuperons les données du client ... "):
            pred = request_prediction(MODEL_URI, str(user_id))
            if type(pred) == dict:

                if "error" in pred:
                    st.write(f"")
                    st.write(f"Erreur {pred['error']}")
                else:
                    jauge = go.Figure(go.Indicator(
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            value = round(pred['risk'],2),
                            mode = "gauge+number+delta",
                            delta = {'reference': Seuil, 'decreasing': {'color': CouleurAccord}, 'increasing': {'color': CouleurRefus}},
                            gauge = {'axis': {'range': [None, 1]},
                                     'bar': {'color': "#464646", 'thickness': 0.3},
                                     'steps' : [
                                         {'range': [0, Seuil], 'color': CouleurAccord},
                                         {'range': [Seuil, 1], 'color': CouleurRefus}],
                                     'threshold' : {'line': {'color': "white", 'width': 2}, 'thickness': 0.9, 'value': Seuil}}))
                    st.plotly_chart(jauge, use_container_width=False, theme="streamlit", on_select="ignore")
                    st.divider()
                    st.write(f"Prédiction de risque de faillite pour le client {pred['client_id']}")
                    st.write(f"Le seuil de refus est fixé à {Seuil:.2f}")
                    st.write(f"Le risque d'impayés est de {pred['risk']:.2f}")
                    st.write(f"La demande de crédit est {pred['status']}")

                    st.divider()
                    model = loadModel(pathMod+'model.pkl')
                    shap_values_single, shap_values = visualize_importance(model, user_id, ClientsDatabase)
                    st.write(f"Explication Locale")
                    fig, ax = plt.subplots(figsize=(5, 5))
                    shap.plots.waterfall(shap_values_single[0], max_display=10)
                    st.pyplot(fig)

                    st.divider()
                    st.write(f"Explication Globale")
                    fig, ax = plt.subplots(figsize=(5, 5))
                    shap.summary_plot(shap_values, max_display=10)
                    st.pyplot(fig)

if __name__ == '__main__':
    main()