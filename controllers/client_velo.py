#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_velo = Blueprint('client_velo', __name__, template_folder='templates')

@client_velo.route('/client/index')
@client_velo.route('/client/velo/show')              # remplace /client
def client_velo_show():                                 # remplace client_index
    id_client = session['id_user']

    mycursor = get_db().cursor()
    sql = '''SELECT * FROM velo'''
    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " WHERE "
    if 'filter_word' in session:
        sql = sql + " nom_velo LIKE %s "
        recherche = "%" + session['filter_word'] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if 'filter_prix_min' in session or 'filter_prix_max' in session:
        if 'filter_word' in session:
            sql = sql + condition_and + 'prix_velo BETWEEN %s AND %s'
        else:
            sql = sql + 'prix_velo BETWEEN %s AND %s'
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
    tuple_sql = tuple(list_param)
    mycursor.execute(sql, tuple_sql)
    velos = mycursor.fetchall()
    sql3 = ''' prise en compte des commentaires et des notes dans le SQL    '''

    sql = ''' SELECT * FROM type_velo '''
    mycursor.execute(sql)
    types_velo = mycursor.fetchall()

    sql = '''SELECT * FROM ligne_panier
             LEFT JOIN velo ON velo.id_velo = ligne_panier.velo_id
             WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    velos_panier = mycursor.fetchall()

    if len(velos_panier) >= 1:
        sql = '''SELECT SUM(prix*quantite_commande) FROM ligne_commande AS prix_total'''
        mycursor.execute(sql)
        prix_total_panier = mycursor.fetchone()
    else:
        prix_total_panier = 0
    return render_template('client/boutique/panier_velo.html', velos=velos, types_velo=types_velo, velos_panier=velos_panier, prix_total_panier=prix_total_panier, items_filtre=types_velo)