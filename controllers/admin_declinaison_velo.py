#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_velo = Blueprint('admin_declinaison_velo', __name__, template_folder='templates')


@admin_declinaison_velo.route('/admin/declinaison_velo/add')
def add_declinaison_velo():
    mycursor = get_db().cursor()
    id_velo = request.args.get('id_velo')
    sql = '''SELECT * FROM velo
             WHERE id_velo = %s;'''
    mycursor.execute(sql, (id_velo,))
    velo = mycursor.fetchone()
    sql = '''SELECT id_couleur, libelle_couleur FROM couleur'''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()
    sql = '''SELECT id_taille, libelle_taille FROM taille'''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()
    sql = '''SELECT taille_id, id_declinaison_velo FROM declinaison_velo
             WHERE velo_id = %s'''
    mycursor.execute(sql, (id_velo,))
    d_taille_uniq = mycursor.fetchone()
    if d_taille_uniq is not None:
        taille_id = d_taille_uniq.get('taille_id')
        if taille_id == 1:
            d_taille_uniq = 1
    sql = '''SELECT couleur_id, id_declinaison_velo FROM declinaison_velo
             WHERE velo_id = %s'''
    mycursor.execute(sql, (id_velo,))
    d_couleur_uniq = mycursor.fetchone()
    if d_couleur_uniq is not None:
        couleur_id = d_couleur_uniq.get('couleur_id')
        if couleur_id == 1:
            d_couleur_uniq = 1
    return render_template('admin/velo/add_declinaison_velo.html', velo=velo, couleurs=couleurs, tailles=tailles, d_taille_uniq=d_taille_uniq, d_couleur_uniq=d_couleur_uniq)


@admin_declinaison_velo.route('/admin/declinaison_velo/add', methods=['POST'])
def valid_add_declinaison_velo():
    mycursor = get_db().cursor()
    stock_declinaison = request.form.get('stock')
    id_velo = request.form.get('id_velo')
    taille = request.form.get('taille', '')
    couleur = request.form.get('couleur', '')
    tuple_select = (id_velo, taille, couleur)
    sql = '''SELECT * FROM declinaison_velo
             WHERE velo_id = %s AND taille_id = %s AND couleur_id = %s'''
    mycursor.execute(sql, tuple_select)
    declinaisonpresent = mycursor.fetchall()
    if declinaisonpresent is None:
        tuple_insert = (stock_declinaison, id_velo, taille, couleur)
        sql = '''INSERT INTO declinaison_velo(id_declinaison_velo, stock, velo_id, taille_id, couleur_id) VALUES (NULL, %s, %s, %s, %s)'''
        mycursor.execute(sql, tuple_insert)
    else:
        tuple_update = (stock_declinaison, id_velo, taille, couleur)
        sql = '''UPDATE declinaison_velo SET stock = %s
                 WHERE velo_id = %s AND taille_id = %s AND couleur_id = %s'''
        mycursor.execute(sql, tuple_update)
        flash('doublon sur cette déclinaison, seul le stock a été mise à jour', 'alert-warning')
    get_db().commit()
    return redirect('/admin/velo/edit?id_velo=' + id_velo)


@admin_declinaison_velo.route('/admin/declinaison_velo/edit', methods=['POST'])
def valid_edit_declinaison_velo():
    mycursor = get_db().cursor()
    id_declinaison_velo = request.form.get('id_declinaison_velo', '')
    id_velo = request.form.get('id_velo', '')
    stock_declinaison = request.form.get('stock_declinaison', '')
    taille_id = request.form.get('taille_id', '')
    couleur_id = request.form.get('couleur_id', '')
    tuple_update = (stock_declinaison, id_velo, taille_id, couleur_id, id_declinaison_velo)
    sql = '''UPDATE declinaison SET stock_declinaison = %s, velo_id = %s, taille_id = %s, couleur_id = %s
             WHERE id_declinaison_velo = %s'''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    message = u'declinaison_velo modifié , id:' + str(id_declinaison_velo) + '- stock :' + str(stock_declinaison) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/velo/edit?id_velo=' + str(id_velo))


@admin_declinaison_velo.route('/admin/declinaison_velo/edit', methods=['POST'])
def valid_edit_declinaison_velo():
    id_declinaison_velo = request.form.get('id_declinaison_velo','')
    id_velo = request.form.get('id_velo','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()

    message = u'declinaison_velo modifié , id:' + str(id_declinaison_velo) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/velo/edit?id_velo=' + str(id_velo))


@admin_declinaison_velo.route('/admin/declinaison_velo/delete', methods=['GET'])
def admin_delete_declinaison_velo():
    id_declinaison_velo = request.args.get('id_declinaison_velo','')
    id_velo = request.args.get('id_velo','')

    flash(u'declinaison supprimée, id_declinaison_velo : ' + str(id_declinaison_velo),  'alert-success')
    return redirect('/admin/velo/edit?id_velo=' + str(id_velo))
