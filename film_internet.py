#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:04:11 2026

@author: killianboutal
"""

import random as rd
import pandas as pd
import gspread as gs
import streamlit as sl
from gspread_dataframe import set_with_dataframe
import plotly.express as px

if 'film_choisi' not in sl.session_state:
    sl.session_state.film_choisi = ''
if 'film_en_attente' not in sl.session_state:
    sl.session_state.film_en_attente = False
if 'utilisateur' not in sl.session_state:
    sl.session_state.utilisateur = ''

sl.markdown("""
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/Sophren314/selecteur-de-film/main/IMG_0144.jpeg");
        background-size: cover;
        background-position: center;
    }
    .stButton > button {
        background-color: #F0FFFF;
        opacity: 0.8;
        color: black;
        border-radius: 20px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.1);
        box-shadow: 0px 0px 15px #FF4B4B;
    }
    </style>
""", unsafe_allow_html=True)

credentials = sl.secrets["gcp_service_account"]
client = gs.service_account_from_dict(credentials)
sheet = client.open('liste de film')
feuille = sheet.sheet1

reponse1 = 'ajoute des films nullos'
reponse2 = 'le film a regarder est: '
reponse3 = 'pense a ajouter des films nigaud'
reponse4 = 'vous avez tout regarder ensemble !!'

film = pd.DataFrame(feuille.get_all_records())
films = film['films']
killian = film['Killian']
angela = film['Angela']

sl.title('Sélecteur de film 🎬')

if sl.session_state.film_en_attente == False:
    col1, col2, col3 = sl.columns(3)
    with col1:
        if sl.button('Killian', use_container_width=True):
            mask = killian == 'O'
            film_filtre = films[mask]
            if len(film_filtre) == 0:
                sl.write(reponse4)
            else:
                sl.session_state.film_choisi = rd.choice(film_filtre.tolist())
                sl.session_state.utilisateur = 'Killian'
                sl.session_state.film_en_attente = True
                sl.rerun()

    with col2:
        if sl.button('Nous deux', use_container_width=True):
            mask = (killian == 'O') & (angela == 'O')
            film_filtre = films[mask]
            if len(film_filtre) == 0:
                sl.write(reponse4)
            else:
                sl.session_state.film_choisi = rd.choice(film_filtre.tolist())
                sl.session_state.utilisateur = 'Nous deux'
                sl.session_state.film_en_attente = True
                sl.rerun()

    with col3:
        if sl.button('Angela', use_container_width=True):
            mask = angela == 'O'
            film_filtre = films[mask]
            if len(film_filtre) == 0:
                sl.write(reponse4)
            else:
                sl.session_state.film_choisi = rd.choice(film_filtre.tolist())
                sl.session_state.utilisateur = 'Angela'
                sl.session_state.film_en_attente = True
                sl.rerun()

if sl.session_state.film_en_attente == True:
    if len(films) < 20:
        sl.warning(reponse3)
    sl.success(reponse2 + sl.session_state.film_choisi)

    col1, col2 = sl.columns(2)
    with col1:
        if sl.button('🔄 Refaire', use_container_width=True):
            if sl.session_state.utilisateur == 'Killian':
                mask = killian == 'O'
            elif sl.session_state.utilisateur == 'Angela':
                mask = angela == 'O'
            elif sl.session_state.utilisateur == 'Nous deux':
                mask = (killian == 'O') & (angela == 'O')
            film_filtre = films[mask]
            if len(film_filtre) == 0:
                sl.write(reponse4)
            else:
                sl.session_state.film_choisi = rd.choice(film_filtre.tolist())
                sl.rerun()

    with col2:
        if sl.button('✅ Valider', use_container_width=True):
            film_choisi = sl.session_state.film_choisi
            utilisateur = sl.session_state.utilisateur
            if utilisateur == 'Killian':
                film.loc[film['films'] == film_choisi, 'Killian'] = 'X'
            elif utilisateur == 'Angela':
                film.loc[film['films'] == film_choisi, 'Angela'] = 'X'
            elif utilisateur == 'Nous deux':
                film.loc[film['films'] == film_choisi, 'Killian'] = 'X'
                film.loc[film['films'] == film_choisi, 'Angela'] = 'X'
            index_film = film[film['films'] == film_choisi].index[0]
            val_killian = film.loc[index_film, 'Killian']
            val_angela = film.loc[index_film, 'Angela']
            if val_angela == 'X' and val_killian == 'X':
                film = film[film['films'] != film_choisi]
            feuille.clear()
            set_with_dataframe(feuille, film)
            sl.session_state.film_en_attente = False
            sl.session_state.film_choisi = ''
            sl.session_state.utilisateur = ''
            sl.rerun()

killian_vu = len(film[film['Killian'] == 'X'])
angela_vu = len(film[film['Angela'] == 'X'])

sl.metric(label='il reste au total :' , value = len(films))

graph = pd.DataFrame({
    'Personne': ['Killian', 'Angela'],
    'Films vus': [killian_vu, angela_vu]
})

fig = px.bar(graph, x='Personne', y='Films vus', title='Films vus par personne',
             color='Personne',
             color_discrete_sequence=['#FFFFFF', '#FF80FF'])
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
fig.update_traces(marker_line_width=1.5)
sl.plotly_chart(fig, use_container_width=True)
