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

credentials = '/Users/killianboutal/Desktop/programmation/selecteur-film-ec404726c593.json'
client = gs.service_account(filename=credentials)
sheet= client.open('liste de film')
feuille = sheet.sheet1

reponse1 = 'ajoute des films nullos'
reponse2 = 'le film a regarder est: '
reponse3 = 'pense a ajouter des films nigaud'
reponse4 ='vous avez tout regarder ensemble !!'


film = pd.DataFrame(feuille.get_all_records())

films = film['films']
killian = film['Killian']
angela = film['Angela']

if len(films) == 0:
    print(reponse1)
else:    
    if  sl.button('Killian'):
        mask = killian == 'O'
    elif sl.button('Angela'):
        mask = angela == 'O'
    elif sl.button('nous deux'):
        mask = (killian == 'O') & (angela == 'O')
    
    film_filtre = films[mask]
    
    
    if len(film_filtre) == 0:
        print(reponse4)
    else:
        film_choisi = rd.choice(film_filtre.tolist())
    
        if len(films) < 20:
            print(reponse3)
        print(reponse2 + "' " + film_choisi + "'")
        if sl.button('Killian'):
            film.loc[film['films'] == film_choisi, 'Killian'] = 'X'
        elif sl.button('Angela'):
            film.loc[film['films'] == film_choisi, 'Angela'] = 'X'
        elif sl.button('nous deux'):
            film.loc[film['films'] == film_choisi, 'Killian'] = 'X'
            film.loc[film['films'] == film_choisi, 'Angela'] = 'X'
        
        index_film = film[film['films'] == film_choisi].index[0]
    
        val_killian = film.loc[index_film, 'Killian']
    
        val_angela = film.loc[index_film, 'Angela']
    
        if val_angela == 'X' and val_killian == 'X':
            film = film[film['films'] != film_choisi]
feuille.clear()
feuille.update([film.columns.tolist()] + film.values.tolist())
            
            
            
            
            
            
            
            
            
            