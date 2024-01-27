#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_velo = request.form.get('id_velo')
    quantite = request.form.get('quantite')
    # ---------
    #id_declinaison_velo=request.form.get('id_declinaison_velo',None)
    id_declinaison_velo = 1

# ajout dans le panier d'une déclinaison d'un velo (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_velo))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_velo = declinaisons[0]['id_declinaison_velo']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_velo))
    #     velo = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_velo.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , velo=velo)

# ajout dans le panier d'un velo


    return redirect('/client/velo/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_velo = request.form.get('id_velo','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'velo
    # id_declinaison_velo = request.form.get('id_declinaison_velo', None)

    sql = ''' selection de la ligne du panier pour le velo et l'utilisateur connecté'''
    velo_panier=[]

    if not(velo_panier is None) and velo_panier['quantite'] > 1:
        sql = ''' mise à jour de la quantité dans le panier => -1 velo '''
    else:
        sql = ''' suppression de la ligne de panier'''

    # mise à jour du stock de l'velo disponible
    get_db().commit()
    return redirect('/client/velo/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' sélection des lignes de panier'''
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier du velo pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock du velo : stock = stock + qté de la ligne pour le velo'''
        get_db().commit()
    return redirect('/client/velo/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_velo = request.form.get('id_declinaison_velo')

    sql = ''' selection de ligne du panier '''

    sql = ''' suppression de la ligne du panier '''
    sql2=''' mise à jour du stock du velo : stock = stock + qté de la ligne pour le velo'''

    get_db().commit()
    return redirect('/client/velo/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    return redirect('/client/velo/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/velo/show')
