#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''SELECT id_commande, etat_id, login, date_achat, SUM(quantite_commande) as nbr_velos, SUM(velo.prix_velo * quantite_commande) as prix_total, etat.libelle_etat as libelle
    FROM commande 
    JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
    JOIN etat ON commande.etat_id = etat.id_etat
    JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
    JOIN velo ON ligne_commande.velo_id = velo.id_velo
    GROUP BY id_commande, etat_id, login, date_achat, etat.libelle_etat
    ORDER BY etat_id, date_achat DESC  '''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()
#
    commande_id = request.args.get('id_commande', None)
    sql2 = '''SELECT velo.nom_velo AS nom, quantite_commande AS quantite, (velo.prix_velo * quantite_commande) AS prix_ligne, velo.prix_velo AS prix
              FROM ligne_commande 
              LEFT JOIN velo ON ligne_commande.velo_id = velo.id_velo
              WHERE commande_id = %s'''
    mycursor.execute(sql2, (commande_id,))
    velos_commande = mycursor.fetchall()

    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande != None:
        sql = '''SELECT * FROM commande WHERE id_commande = %s;'''
        mycursor.execute(sql, (id_commande,))
        commande_adresses = mycursor.fetchall()

    return render_template('admin/commandes/show.html', commandes=commandes, velos_commande=velos_commande, commande_adresses=commande_adresses)


@admin_commande.route('/admin/commande/valider', methods=['get', 'post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''UPDATE commande SET etat_id=2 WHERE  id_commande=%s'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')