#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__, template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT *, velo.prix_velo FROM ligne_panier
            LEFT JOIN velo ON ligne_panier.velo_id = velo.id_velo
            WHERE utilisateur_id=%s'''
    mycursor.execute(sql, (id_client,))
    velos_panier = mycursor.fetchall()
    if len(velos_panier) >= 1:
        sql = '''SELECT SUM(velo.prix_velo*quantite_panier) AS prix_commande FROM ligne_panier
                LEFT JOIN velo ON ligne_panier.velo_id = velo.id_velo
                WHERE utilisateur_id=%s'''
        mycursor.execute(sql, (id_client,))
        prix_total = mycursor.fetchone()['prix_commande']
    else:
        prix_total = 0
    sql = '''SELECT * FROM adresse
            WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    adresses = mycursor.fetchall()
    return render_template('client/boutique/panier_validation_adresses.html', adresses=adresses, velos_panier=velos_panier, prix_total=prix_total, validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )

@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_livraison = request.form.get('id_adresse_livraison')
    id_facturation = request.form.get('id_adresse_livraison')
    id_client = session['id_user']
    sql = '''SELECT *, velo.prix_velo FROM ligne_panier
            JOIN velo ON ligne_panier.velo_id = velo.id_velo
            WHERE utilisateur_id=%s;'''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'velos dans le ligne_panier', 'alert-warning')
        return redirect('/client/velo/show')
    # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    #a = datetime.strptime('my date', "%b %d %Y %H:%M")

    sql = '''INSERT INTO commande(date_achat, utilisateur_id, etat_id) VALUES (NOW(), %s, 1);'''
    mycursor.execute(sql, (id_client,))
    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    derniere_commande = mycursor.fetchone()['last_insert_id']
    for item in items_ligne_panier:
        id_velo = item['velo_id']
        prix_commande = item['prix_velo']
        quantite_commande = item['quantite_panier']
        sql = '''DELETE FROM ligne_panier
                  WHERE velo_id = %s AND utilisateur_id = %s;'''
        mycursor.execute(sql, (id_velo, id_client,))
        sql = '''INSERT INTO ligne_commande(commande_id, velo_id, prix, quantite_commande) VALUES(%s, %s, %s, %s);'''
        mycursor.execute(sql, (derniere_commande, id_velo, prix_commande, quantite_commande,))
    get_db().commit()
    flash(u'Commande ajoutée', 'alert-success')
    return redirect('/client/velo/show')



@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT id_commande, etat_id, date_achat, SUM(ligne_commande.quantite_commande) AS nbr_velos, SUM(ligne_commande.prix * ligne_commande.quantite_commande) AS prix_total, etat.libelle_etat
            FROM commande
            LEFT JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
            LEFT JOIN etat ON commande.etat_id = etat.id_etat
            WHERE utilisateur_id = %s
            GROUP BY id_commande, etat_id, date_achat, etat.libelle_etat   
            ORDER BY etat_id, date_achat DESC;'''
    mycursor.execute(sql, (id_client, ))
    commandes = mycursor.fetchall()

    velos_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = '''SELECT velo.nom_velo AS nom, quantite_commande AS quantite_commande, (prix * quantite_commande) AS prix_total, prix AS prix_velo
                 FROM ligne_commande 
                 LEFT JOIN velo ON ligne_commande.velo_id = velo.id_velo
                 WHERE commande_id = %s
                 '''
        mycursor.execute(sql, (id_commande,))
        velos_commande = mycursor.fetchall()

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''''''

    return render_template('client/commandes/show.html', commandes=commandes, velos_commande=velos_commande, commande_adresses=commande_adresses)
