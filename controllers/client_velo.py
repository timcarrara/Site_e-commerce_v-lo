#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import render_template, session

from connexion_db import get_db

client_velo = Blueprint('client_velo', __name__, template_folder='templates')


@client_velo.route('/client/index')
@client_velo.route('/client/velo/show')  # remplace /client
def client_velo_show():  # remplace client_index
    id_client = session['id_user']

    mycursor = get_db().cursor()
    sql = '''SELECT id_velo, nom_velo, velo.image, prix_velo,
        SUM(stock) AS stock, COUNT(id_declinaison_velo) AS nb_declinaison
        FROM declinaison_velo
        JOIN velo ON declinaison_velo.velo_id = velo.id_velo
        '''
    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " WHERE "
    if 'filter_word' in session:
        sql = sql + " nom_velo Like %s "
        recherche = "%" + session['filter_word'] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if 'filter_prix_min' in session or 'filter_prix_max' in session:
        sql = sql + condition_and + 'prix_velo BETWEEN %s AND %s'
        list_param.append(session['filter_prix_min'])
        list_param.append(session['filter_prix_max'])
        condition_and = " AND "
    if 'filter_types' in session:
        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sql = sql + "type_velo_id=%s"
            if item != last_item:
                sql = sql + " OR "
            list_param.append(item)
        sql = sql + ")"
    sql += "GROUP BY id_velo"
    tuple_sql = tuple(list_param)
    mycursor.execute(sql, tuple_sql)
    velos = mycursor.fetchall()

    sql = '''SELECT * FROM type_velo;'''
    mycursor.execute(sql)
    types_velo = mycursor.fetchall()

    sql = '''SELECT nom_velo, quantite_panier, prix_velo, stock, id_declinaison_velo, id_velo, id_couleur, 
             id_taille, libelle_couleur, libelle_taille
             FROM ligne_panier
             LEFT JOIN declinaison_velo ON ligne_panier.velo_declinaison_id = declinaison_velo.id_declinaison_velo
             LEFT JOIN velo ON declinaison_velo.velo_id = velo.id_velo
             LEFT JOIN couleur ON declinaison_velo.couleur_id = couleur.id_couleur
             LEFT JOIN taille ON declinaison_velo.taille_id = taille.id_taille
             WHERE utilisateur_id = %s;'''
    mycursor.execute(sql, (id_client,))
    velos_panier = mycursor.fetchall()
    print(velos_panier)

    prix_total = None
    if len(velos_panier) >= 1:
        sql = '''SELECT SUM(prix_declinaison*quantite_panier) AS prix_total 
        FROM ligne_panier
        LEFT JOIN declinaison_velo ON ligne_panier.velo_declinaison_id = declinaison_velo.id_declinaison_velo
        WHERE utilisateur_id = %s;'''
        mycursor.execute(sql, (id_client,))
        prix_total = mycursor.fetchone()['prix_total']

    return render_template('client/boutique/panier_velo.html', velos=velos, types_velo=types_velo,
                           velos_panier=velos_panier, prix_total=prix_total, items_filtre=types_velo)
