#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__, template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    utilisateur_id = session['id_user']
    id_velo = request.form.get('id_velo')
    quantite_panier = request.form.get('quantite')
    id_declinaison_velo = request.form.get('id_declinaison_velo')

    if quantite_panier == '0':
        flash(u'La quantité doit être supérieure à 0', 'alert-warning')
        return redirect('/client/velo/show')

    if id_declinaison_velo is None:
        sql = '''SELECT * 
                 FROM declinaison_velo
                 LEFT JOIN velo ON declinaison_velo.velo_id = velo.id_velo
                 LEFT JOIN couleur ON declinaison_velo.couleur_id = couleur.id_couleur
                 LEFT JOIN taille ON declinaison_velo.taille_id = taille.id_taille
                 WHERE id_velo = %s
            '''
        mycursor.execute(sql, (id_velo,))
    else:
        sql = '''SELECT * FROM declinaison_velo
                 WHERE id_declinaison_velo = %s
            '''
        mycursor.execute(sql, (id_declinaison_velo,))
    declinaisons = mycursor.fetchall()

    if len(declinaisons) == 1:
        id_declinaison_velo = declinaisons[0]['id_declinaison_velo']

        sql = """SELECT * FROM ligne_panier
                 WHERE utilisateur_id = %s AND velo_declinaison_id = %s
                """
        mycursor.execute(sql, (utilisateur_id, id_declinaison_velo))
        velopresent = mycursor.fetchone()
        if velopresent is None:
            sql = """INSERT INTO ligne_panier (utilisateur_id, velo_declinaison_id, date_ajout, quantite_panier) 
                     VALUES (%s, %s, NOW(), %s)"""
            mycursor.execute(sql, (utilisateur_id, id_declinaison_velo, quantite_panier))
        else:
            sql = """UPDATE ligne_panier SET quantite_panier = quantite_panier + %s
                     WHERE velo_declinaison_id = %s AND utilisateur_id = %s"""
            mycursor.execute(sql, (quantite_panier, id_declinaison_velo, utilisateur_id))

        sql = """UPDATE declinaison_velo SET stock = stock - %s
                 WHERE id_declinaison_velo = %s"""
        mycursor.execute(sql, (quantite_panier, id_declinaison_velo))

    elif len(declinaisons) == 0:
        abort('pb nb de declinaison')
    else:
        sql = '''SELECT id_velo, nom_velo, prix_velo, image
                 FROM velo 
                 WHERE id_velo = %s'''
        mycursor.execute(sql, (id_velo,))
        velo = mycursor.fetchone()
        return render_template('client/boutique/declinaison_velo.html', declinaisons=declinaisons, velo=velo)
    get_db().commit()
    return redirect('/client/velo/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison_velo = request.form.get('id_declinaison_velo')

    sql = '''SELECT * FROM ligne_panier
             WHERE velo_declinaison_id = %s AND utilisateur_id = %s;'''
    mycursor.execute(sql, (id_declinaison_velo, id_client,))
    velo_panier = mycursor.fetchone()

    if not (velo_panier is None) and velo_panier['quantite_panier'] > 1:
        sql = '''UPDATE ligne_panier SET quantite_panier = quantite_panier - 1
                 WHERE velo_declinaison_id = %s AND utilisateur_id = %s;'''
        mycursor.execute(sql, (id_declinaison_velo, id_client,))

    else:
        sql = '''DELETE FROM ligne_panier
                 WHERE velo_declinaison_id = %s AND utilisateur_id = %s;'''
        mycursor.execute(sql, (id_declinaison_velo, id_client,))

    sql = '''UPDATE declinaison_velo SET stock = stock + 1
             WHERE id_declinaison_velo = %s;'''
    mycursor.execute(sql, (id_declinaison_velo,))
    get_db().commit()
    return redirect('/client/velo/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = '''SELECT * FROM ligne_panier'''
    mycursor.execute(sql)
    items_panier = mycursor.fetchall()
    for item in items_panier:
        id_declinaison_velo = item['velo_declinaison_id']
        quantite_panier = item['quantite_panier']
        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s'''
        mycursor.execute(sql, (client_id,))
        sql2 = '''UPDATE declinaison_velo SET stock = stock + %s
                  WHERE id_declinaison_velo =%s'''
        mycursor.execute(sql2, (quantite_panier, id_declinaison_velo,))
        get_db().commit()
    return redirect('/client/velo/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison_velo = request.form.get('id_declinaison_velo')
    sql_select = '''SELECT * FROM ligne_panier
                    WHERE utilisateur_id = %s AND velo_declinaison_id = %s'''
    mycursor.execute(sql_select, (id_client, id_declinaison_velo))
    velo_panier = mycursor.fetchone()
    sql_delete = '''DELETE FROM ligne_panier 
                    WHERE utilisateur_id=%s AND velo_declinaison_id =%s'''
    mycursor.execute(sql_delete, (id_client, id_declinaison_velo))
    sql_update = '''UPDATE declinaison_velo 
                    SET stock = stock + %s
                    WHERE id_declinaison_velo = %s'''
    mycursor.execute(sql_update, (velo_panier['quantite_panier'], id_declinaison_velo))
    get_db().commit()
    return redirect('/client/velo/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types')
    print("word : " + filter_word + str(len(filter_word)))
    if filter_word or filter_word == '':
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u'Votre mot doit être composé uniquement de lettres', 'alert-danger')
        else:
            if len(filter_word) == 1:
                flash(u"Votre mot recherché doit être composé d'au moins deux lettres", 'alert-danger')
            else:
                session.pop('filter_hotel', None)

    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'Le prix minimum doit être inférieur au prix maximum', 'alert-danger')
        else:
            flash(u'Les prix minimum et maximum doivent être des numériques', 'alert-danger')
    if filter_types and filter_types != []:
        session['filter_types'] = filter_types
    return redirect('/client/velo/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/velo/show')
