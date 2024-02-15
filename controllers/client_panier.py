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

    sql = '''SELECT quantite_panier FROM ligne_panier 
             WHERE velo_id = %s AND utilisateur_id = %s;'''
    mycursor.execute(sql, (id_velo, utilisateur_id,))
    velopresent = mycursor.fetchone()

    if velopresent is None:
        if quantite_panier == '0':
            flash(u'la quantité doit être un numérique et supérieure à 0', 'alert-warning')
        else:
            sql = '''INSERT INTO ligne_panier (utilisateur_id, velo_id, date_ajout, quantite_panier) 
                    VALUES (%s, %s, NOW(), %s);'''
            mycursor.execute(sql, (utilisateur_id, id_velo, quantite_panier,))
            get_db().commit()
            print("if")

    else:
        sql = '''UPDATE ligne_panier SET quantite_panier = quantite_panier + %s
                 WHERE velo_id = %s AND utilisateur_id = %s;'''
        mycursor.execute(sql, (quantite_panier, id_velo, utilisateur_id,))
        get_db().commit()
        print("else")

    sql = '''UPDATE velo SET stock = stock - %s
             WHERE id_velo = %s;'''
    mycursor.execute(sql, (quantite_panier, id_velo,))

    get_db().commit()





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
    id_velo = request.form.get('id_velo')
    quantite_panier = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'boisson
    # id_declinaison_boisson = request.form.get('id_declinaison_boisson', None)

    sql = ''' SELECT * FROM ligne_panier
              WHERE velo_id = %s AND utilisateur_id = %s;'''
    mycursor.execute(sql, (id_velo, id_client,))
    velo_panier = mycursor.fetchone()

    if not (velo_panier is None) and velo_panier['quantite_panier'] > 1:
        sql = '''UPDATE ligne_panier SET quantite_panier = ligne_panier.quantite_panier - 1
                WHERE velo_id = %s AND utilisateur_id = %s;'''
        mycursor.execute(sql, (id_velo, id_client,))

    else:
        sql = ''' DELETE FROM ligne_panier
                  WHERE velo_id = %s AND utilisateur_id = %s;'''
        mycursor.execute(sql, (id_velo, id_client,))

    sql = '''UPDATE velo SET stock = stock + 1
             WHERE id_velo = %s;'''
    mycursor.execute(sql, (id_velo, ))
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
        id_velo = item['velo_id']
        quantite_panier = item['quantite_panier']
        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s'''
        mycursor.execute(sql, (client_id,))
        sql2 = '''UPDATE velo SET stock = stock + %s
                  WHERE id_velo =%s'''
        mycursor.execute(sql2, (quantite_panier, id_velo,))
        get_db().commit()
    return redirect('/client/velo/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_velo = request.form.get('id_velo')
    sql_select = '''SELECT * FROM ligne_panier
                    WHERE utilisateur_id = %s AND velo_id = %s'''
    mycursor.execute(sql_select, (id_client, id_velo))
    velo_panier = mycursor.fetchone()
    sql_delete = '''DELETE FROM ligne_panier 
                    WHERE utilisateur_id=%s AND velo_id=%s'''
    mycursor.execute(sql_delete, (id_client, id_velo))
    sql_update = '''UPDATE velo 
                    SET stock = stock + %s
                    WHERE id_velo = %s'''
    mycursor.execute(sql_update, (velo_panier['quantite_panier'], id_velo))
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
