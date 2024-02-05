#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_velo = Blueprint('client_velo', __name__, template_folder='templates')

#@client_velo.route('/client/index')
@client_velo.route('/client/velo/show')              # remplace /client
def client_velo_show():                                 # remplace client_index
    #id_client = session['id_user']
    print("Starting the route function")

    mycursor = get_db().cursor()
    sql = '''SELECT * FROM velo'''
    mycursor.execute(sql)
    velo = mycursor.fetchall()

    sql = '''SELECT * FROM type_velo'''
    mycursor.execute(sql)
    typeVelo = mycursor.fetchall()

    print("Database query executed successfully")

    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_types" in session or "filter_prix_min" in session or "filter_prix_max" in session:
        sql = sql + " WHERE "
    if 'filter_hotel' in session:
        sql = sql + " nom_velo Like %s "
        recherche = "%" + session['filter_hotel'] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if 'filter_prixminimum' in session or 'filter_prixmaximum' in session:
        sql = sql + condition_and + 'prix_base_chambre BETWEEN %s AND %s'
        list_param.append(session['filter_prixminimum'])
        list_param.append(session['filter_prixmaximum'])
        condition_and = " AND "
    if 'filter_station' in session:
        sql = sql + condition_and + "("
        last_item = session['filter_station'][-1]
        for item in session['filter_station']:
            sql = sql + "station_id=%s"
            if item != last_item:
                sql = sql + " OR "
            list_param.append(item)
        sql = sql + ")"
    # utilisation du filtre
    #sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    #velos =[]

    # pour le filtre
    #types_velo = []

    #velos_panier = []

    #if len(velos_panier) >= 1:
    #    sql = ''' calcul du prix total du panier '''
    #    prix_total = None
    #else:
    #    prix_total = None
    return render_template('client/boutique/panier_velo.html', velos=velo, typeVelo=typeVelo)

#                           #, velos_panier=velos_panier
                           #, prix_total=prix_total
                           #, items_filtre=type_velo