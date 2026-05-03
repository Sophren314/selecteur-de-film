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
    border-radius:20px;
    border: none;
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

col1,col2,col3 = sl.columns(3)
with col2:
    pass

if len(films) == 0:
    sl.write(reponse1)
else:
    with col3:
        if sl.button('Killian'):
            mask = killian == 'O'
            film_filtre = films[mask]
            if len(film_filtre) == 0:
                sl.write(reponse4)
            else:
                film_choisi = rd.choice(film_filtre.tolist())
                if len(films) < 20:
                    sl.write(reponse3)
                sl.write(reponse2 + film_choisi)
                film.loc[film['films'] == film_choisi, 'Killian'] = 'X'
                index_film = film[film['films'] == film_choisi].index[0]
                val_killian = film.loc[index_film, 'Killian']
                val_angela = film.loc[index_film, 'Angela']
                if val_angela == 'X' and val_killian == 'X':
                    film = film[film['films'] != film_choisi]
                feuille.clear()
                set_with_dataframe(feuille, film)
    with col1:
        if sl.button('Angela'):
            mask = angela == 'O'
            film_filtre = films[mask]
            if len(film_filtre) == 0:
                sl.write(reponse4)
            else:
                film_choisi = rd.choice(film_filtre.tolist())
                if len(films) < 20:
                    sl.write(reponse3)
                sl.write(reponse2 + film_choisi)
                film.loc[film['films'] == film_choisi, 'Angela'] = 'X'
                index_film = film[film['films'] == film_choisi].index[0]
                val_killian = film.loc[index_film, 'Killian']
                val_angela = film.loc[index_film, 'Angela']
                if val_angela == 'X' and val_killian == 'X':
                    film = film[film['films'] != film_choisi]
                feuille.clear()
                set_with_dataframe(feuille, film)
                
with col1:
    pass
with col3:
    pass
with col2:
    if sl.button('Nous deux'):
        mask = (killian == 'O') & (angela == 'O')
        film_filtre = films[mask]
        if len(film_filtre) == 0:
            sl.write(reponse4)
        else:
            film_choisi = rd.choice(film_filtre.tolist())
            if len(films) < 20:
                sl.write(reponse3)
            sl.write(reponse2 + film_choisi)
            film.loc[film['films'] == film_choisi, 'Killian'] = 'X'
            film.loc[film['films'] == film_choisi, 'Angela'] = 'X'
            index_film = film[film['films'] == film_choisi].index[0]
            val_killian = film.loc[index_film, 'Killian']
            val_angela = film.loc[index_film, 'Angela']
            if val_angela == 'X' and val_killian == 'X':
                film = film[film['films'] != film_choisi]
            feuille.clear()
            set_with_dataframe(feuille, film)

killian_vu = len(film[film['Killian'] == 'X'])
angela_vu = len(film[film['Angela'] == 'X'])

graph = pd.DataFrame({
    'Personne': ['Killian','Angela'],
    'Films vus': [killian_vu,angela_vu]
})

fig = px.bar(graph, x='Personne', y='Films vus', title='Films vus par personne',
            color_discrete_sequence = ['#FFFFFF','FF80FF'])
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                 width=300, height=400)
fig.update_traces(marker_line_width=1.5)
sl.plotly_chart(fig)


