import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
from PIL import Image
import shap
import lightgbm
from pathlib import Path
import pickle

st.set_page_config(
    page_title = "Acceptation Crédit",
    page_icon = ":material/assured_workload:",
    layout="wide"
    )

def get_file_number(filename):
    """recuperation du seuil etabli lors de l'elaboration du modele"""
    f = open(filename)
    content = f.read()
    value = float(content)
    f.close()
    return value


pathDb = str(Path(__file__).parent)+'/../Api/Data/Db/'
FichierSeuil = str(Path(__file__).parent)+'/../Api/Data/Seuil.txt'
pathMod = str(Path(__file__).parent)+'/../Api/Data/Model/'
pathImg = str(Path(__file__).parent)+'/../Appli/Images/'
ClientsDatabase = pd.read_csv(pathDb+'ClientDatabase.csv')
ClientsList = ClientsDatabase['SK_ID_CURR'].tolist()
Seuil = get_file_number(FichierSeuil)
CouleurRefus = "#FF0051"
CouleurAccord = "#008BFB"
baliseDeb = f'<font color={CouleurAccord}>'
baliseFin = f'</font>'


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
    return shap_values_single, shap_values, explainer


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


def GetItems(dataset):
    """retourne la liste des variables"""
    return list(dataset.columns.values)


def Client(id,dataset):
    """retourne les informations du client"""
    return DropColumns(dataset.loc[dataset.SK_ID_CURR == id])


def set_state(i):
    """sauvegarde l'etat de la session"""
    st.session_state.etat = i


def SearchRightCol(dataset,colname):
    """retourne la valeur de la variable de la matrice one hot"""
    rightCol = [col for col in dataset.columns if colname in col and dataset[col].values != [0]]
    return ''.join(rightCol).replace(colname,"").replace('_'," ")


def definitionCreditCol(prob,Seuil,item):
    Points = round(prob,3) - Seuil
    if prob >= Seuil :
        #crédit refusé
        Couleur = CouleurRefus
        Texte = "au dessus"
    else:
        #crédit accepté
        Couleur = CouleurAccord
        Texte = "en dessous"
    if item == 'baliseDeb':
        sortie = f'<font color={Couleur}>'
    elif item == 'texteJaug':
        sortie = f'<font color={Couleur}>{Texte}</font>'
    elif item == 'points':
        sortie = f'<font color={Couleur}>{abs(round(Points,3))}</font>'
    return sortie


def main():
    #Url Api
    MODEL_URI = 'https://ocp7-api.onrender.com/'
    #fichier données
    #creation de la session
    if 'etat' not in st.session_state:
        st.session_state.etat = 0
    #Menu
    listeMenu = ClientsList
    listeMenu.insert(0, 'Cliquez ici pour choisir')
    user_id = st.sidebar.selectbox('Dossier client :',listeMenu, index=0, on_change=set_state, args=('selectbox',))
    #predict_btn = st.sidebar.button('Calcul du risque', on_click=set_state, args=[user_id])
    st.sidebar.divider()
    st.sidebar.page_link("https://www.ewd.fr/Formation/Data/P7/Drift_du_Modèle.html", label='Visualisation Data Drift')
    #Page
    style_heading = 'text-align: center'
    st.markdown(f"<h2 style='{style_heading}'>Acceptation Crédit Prêt à Dépenser</h2>", unsafe_allow_html=True)

    if st.session_state.etat != 0 and user_id != 'Cliquez ici pour choisir':
        with st.spinner("Merci de patienter, nous reveillons l'Api ... "):
            pred = request_prediction(MODEL_URI, str(user_id))
        if type(pred) == dict:

            if "error" in pred:
                st.write(f"")
                st.write(f"Erreur {pred['error']}")
            else:
                listeVars = GetItems(DropColumns(ClientsDatabase))
                id_client = pred['client_id']
                st.subheader(f"Données client {pred['client_id']}", divider="blue")
                with st.spinner("Merci de patienter, nous recherchons les données du client ... "):
                    style_center = 'text-align: center'
                    style_rubrique = 'text-align: left'#; text-decoration: underline'
                    DetailClient = Client(pred['client_id'],ClientsDatabase)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Genre: {baliseDeb}{DetailClient['CODE_GENDER'].values[0]}{baliseFin}", unsafe_allow_html=True)
                        st.write(f"Age: {baliseDeb}{round(abs(DetailClient['DAYS_BIRTH'].values[0]/365))}{baliseFin}", unsafe_allow_html=True)
                        st.write(f"Status: {baliseDeb}{SearchRightCol(DetailClient,'NAME_FAMILY_STATUS')}{baliseFin}", unsafe_allow_html=True)
                        st.write(f"Education: {baliseDeb}{SearchRightCol(DetailClient,'NAME_EDUCATION_TYPE')}{baliseFin}", unsafe_allow_html=True)
                        st.write(f"Occupation: {baliseDeb}{SearchRightCol(DetailClient,'OCCUPATION_TYPE')}{baliseFin}", unsafe_allow_html=True)
                        if np.isnan(DetailClient['DAYS_EMPLOYED'].values[0]):
                            st.write(f"Profession: {baliseDeb}inconnue{baliseFin}", unsafe_allow_html=True)
                        else:
                            st.write(f"Profession: {baliseDeb}{SearchRightCol(DetailClient,'ORGANIZATION_TYPE')}{baliseFin}", unsafe_allow_html=True)
                            st.write(f"depuis {baliseDeb}{round(abs(DetailClient['DAYS_EMPLOYED'].values[0]/365))}{baliseFin} années", unsafe_allow_html=True)
                        st.write(f"Type d\'habitation: {baliseDeb}{SearchRightCol(DetailClient,'NAME_HOUSING_TYPE')}{baliseFin}", unsafe_allow_html=True)
                        st.write(f"Voiture : {baliseDeb}{DetailClient['FLAG_OWN_CAR'].values[0]}{baliseFin}", unsafe_allow_html=True)
                    with col2:
                        st.write(f"Patrimoine total : {baliseDeb}{DetailClient.AMT_INCOME_TOTAL.values[0]}{baliseFin} $", unsafe_allow_html=True)
                        st.write(f"Type(s) de contrat(s) obtenus:", unsafe_allow_html=True)
                        Contract = SearchRightCol(DetailClient,'NAME_CONTRACT_TYPE').replace("PREV","  \n").replace("MEAN","")
                        st.write(f"{baliseDeb}{Contract}{baliseFin}", unsafe_allow_html=True)
                        st.write(f"Montant: {baliseDeb}{DetailClient['AMT_CREDIT'].values[0]}{baliseFin} $", unsafe_allow_html=True)
                        st.write(f"Montant annuel: {baliseDeb}{DetailClient['AMT_ANNUITY'].values[0]}{baliseFin} $", unsafe_allow_html=True)
                        st.write(f"Ratio credit sur revenus: {baliseDeb}{round(DetailClient['ANNUITY_INCOME_PERC'].values[0],2)}{baliseFin}", unsafe_allow_html=True)

                st.subheader("Résultat de la demande de crédit", divider="blue")
                with st.spinner("Merci de patienter, nous préparons les données du client ... "):
                    st.write(f"<center><h4>La demande de crédit est ",
                            f"{definitionCreditCol(pred['risk'],Seuil,'baliseDeb')}{pred['status']}{baliseFin}",
                            f"</h4></center>", unsafe_allow_html=True)
                    st.write("  \n  \n")

                st.subheader("Risque de défaut de remboursement", divider="blue")
                with st.spinner("Merci de patienter, nous préparons les données du client ... "):
                    st.write(f"<center><i>Le risque de défaut de remboursement est de ",
                             f"{definitionCreditCol(pred['risk'],Seuil,'baliseDeb')}{pred['risk']:.3f}{baliseFin}",
                             f"Le seuil de refus est fixé à ",
                             f"{baliseDeb}{Seuil:.3f}{baliseFin}</i></center>", unsafe_allow_html=True)
                    st.write(f"<center>Le risque est par consequent ",
                            f"{definitionCreditCol(pred['risk'],Seuil,'texteJaug')} de ",
                            f"{definitionCreditCol(pred['risk'],Seuil,'points')} points du seuil maximal fixé</center>", unsafe_allow_html=True)
                    jauge = go.Figure(go.Indicator(
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            value = round(pred['risk'],3),
                            mode = "gauge+number+delta",
                            delta = {'reference': Seuil, 'decreasing': {'color': CouleurAccord}, 'increasing': {'color': CouleurRefus}},
                            gauge = {'axis': {'range': [None, 1]},
                                 'bar': {'color': "#464646", 'thickness': 0.3},
                                 'steps' : [
                                     {'range': [0, Seuil], 'color': CouleurAccord},
                                     {'range': [Seuil, 1], 'color': CouleurRefus}],
                                 'threshold' : {'line': {'color': "white", 'width': 2}, 'thickness': 0.9, 'value': Seuil}}))
                    jauge.update_layout(hoverlabel_align = 'auto',title = f"Jauge d'acceptation du client {id_client}")
                    st.plotly_chart(jauge, use_container_width=True, theme="streamlit", on_select="ignore")

                st.subheader("Comparaison d\'un client", divider="blue")
                with st.spinner("Merci de patienter, nous recherchons les données du client ... "):
                    options = st.multiselect("Choisissez des variables pour les comparer au groupe",
                                            listeVars,
                                            ['AMT_CREDIT','AMT_ANNUITY']
                                            )
                    if len(options) == 0:
                        st.write(f"Choisissez au moins une variable dans le menu déroulant ci-dessus")
                    else:
                        nb_options = len(options)
                        dfGraph = pd.DataFrame()
                        id_user = ClientsDatabase.loc[ClientsDatabase.SK_ID_CURR == pred['client_id']].index[0]
                        dfGraph = ClientsDatabase[options].agg(['min', 'mean', 'max'])
                        dfGraph = dfGraph._append(ClientsDatabase.loc[ClientsDatabase.SK_ID_CURR == pred['client_id'],options])
                        dfGraph.rename(index={id_user:'client'}, inplace=True)
                        dfGraph=dfGraph.T
                        dfGraph['amplitude']=dfGraph['max']-dfGraph['min']
                        dfGraph['100_prc']=1
                        dfGraph['50_prc']=(dfGraph['mean']-dfGraph['min'])/dfGraph['amplitude']
                        dfGraph['client_prc']=(dfGraph['client']-dfGraph['min'])/dfGraph['amplitude']
                        fig = go.Figure(go.Bar(x=dfGraph.index,
                                                     y=dfGraph['100_prc'],
                                                     marker_color=CouleurAccord,
                                                     hovertemplate="100% des clients<extra></extra>",
                                                     name="100% des clients"
                                                     ))
                        marker_size = 300 / nb_options
                        fig.add_scatter(x=dfGraph.index,
                                        y=dfGraph['50_prc'], mode="markers",
                                        marker_symbol="line-ew",
                                        marker_color="white",
                                        marker_line_color="white",
                                        marker_line_width=2, marker_size=marker_size,
                                        hovertemplate="50% des clients<br>Valeur: %{y:.3f}<extra></extra>",
                                        name="50% des clients")
                        marker_size = marker_size / 2
                        name = f"Client {id_client}"
                        fig.add_scatter(x=dfGraph.index,
                                        y=dfGraph['client_prc'], mode="markers",
                                        text=[f"{id_client}" for i in range(nb_options)],
                                        marker=dict(size=marker_size, color=CouleurRefus),
                                        hovertemplate="Client %{text}<br>Valeur: %{y:.3f}<extra></extra>",
                                        name=name)
                        fig.update_layout(hoverlabel_align = 'auto',title = f"Comparaison du client {id_client} par rapport aux autres clients (données exprimées en % des clients)")
                        st.plotly_chart(fig, use_container_width=False, theme="streamlit", on_select="ignore")


                st.subheader("Analyse des relations entre variables", divider="blue")
                with st.spinner("Merci de patienter, nous calculons l'explication des variables ... "):
                    listeVars1 = listeVars.copy()
                    listeVars1.insert(0, 'Cliquez ici pour choisir')
                    var2Analys1 = st.selectbox('Première variable a analyser :',listeVars1, index=0)
                    if var2Analys1 == 'Cliquez ici pour choisir':
                        st.write(f"Choisissez une première variable dans le menu déroulant ci-dessus")
                    else:
                        listeVars2 = listeVars1.copy()
                        listeVars2.remove(var2Analys1)
                        var2Analys2 = st.selectbox('Deuxième variable a analyser :',listeVars2, index=0)
                        if var2Analys2 == 'Cliquez ici pour choisir':
                            st.write(f"Choisissez une deuxième variable dans le menu déroulant ci-dessus")
                        else:
                            model = loadModel(pathMod+'model.pkl')
                            pipeline = model['pipeline']
                            ClientsDatabaseDroped = DropColumns(ClientsDatabase)
                            ClientsDatabaseTransf = pipeline.transform(DropColumns(ClientsDatabaseDroped))
                            varX = ClientsDatabaseTransf[listeVars.index(var2Analys1)]
                            varY = ClientsDatabaseTransf[listeVars.index(var2Analys2)]
                            fig = go.Figure(go.Scatter(x=varX,
                                            y=varY, mode="markers",
                                            marker_symbol="circle",
                                            marker_color=CouleurAccord,
                                            marker_line_color=CouleurAccord,
                                            marker_line_width=3, marker_size=3,
                                            name="Totalité des clients"))
                            name = f"Client {id_client}"
                            clientIndex = ClientsDatabase.loc[ClientsDatabase.SK_ID_CURR == id_client].index[0]
                            varClientX = ClientsDatabaseTransf[clientIndex,listeVars.index(var2Analys1)]
                            varClientY = ClientsDatabaseTransf[clientIndex,listeVars.index(var2Analys2)]
                            fig.add_scatter(x=[varClientX],
                                        y=[varClientY], mode="markers",
                                        text=[f"{id_client}"],
                                        marker=dict(size=15, color=CouleurRefus),
                                        hovertemplate="Client %{text}<br>Valeur: %{x:.3f} %{y:.3f}<extra></extra>",
                                        name=name)
                            fig.update_layout(hoverlabel_align = 'auto',title = f"Graphique des relations entre {var2Analys2} et {var2Analys1} (données normalisées)")
                            fig.update_xaxes(title_text=var2Analys1)
                            fig.update_yaxes(title_text=var2Analys2)
                            st.plotly_chart(fig, use_container_width=False, theme="streamlit", on_select="ignore")


                with st.spinner("Merci de patienter, nous calculons l'importance des variables ... "):
                    model = loadModel(pathMod+'model.pkl')
                    shap_values_single, shap_values, explainer = visualize_importance(model, user_id, ClientsDatabase)


                st.subheader("Explication Locale", divider="blue")
                st.markdown(f"<center>Influence des données de l'utilisateur sur la décision finale</center>", unsafe_allow_html=True)
                with st.spinner("Merci de patienter, nous calculons l'explication locale ... "):
                    fig, ax = plt.subplots(figsize=(5, 5))
                    shap.plots.waterfall(shap_values_single[0], max_display=10)
                    st.pyplot(fig)

                st.subheader("Explication Globale", divider="blue")
                st.markdown(f"<center>Données agissant principalement sur le modèle</center>", unsafe_allow_html=True)
                with st.spinner("Merci de patienter, nous calculons l'explication globale ... "):
                    fig, ax = plt.subplots(figsize=(5, 5))
                    shap.summary_plot(shap_values, max_display=10)
                    #fig.title(f"Principales influences sur le modèle")
                    st.pyplot(fig)
    else:
        st.write('')
        st.markdown(f"<center>Cet outil sert a valider l'acceptation des crédits</center>", unsafe_allow_html=True)
        st.markdown(f"<center>Il fourni une probabilité de non solvabilité d'un client</center>", unsafe_allow_html=True)
        st.markdown(f"<center>Pour lancer une analyse, selectionnez un client dans la liste</center>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()