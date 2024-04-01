#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import render_template

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__, template_folder='templates')


@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_velo_stock():
    mycursor = get_db().cursor()

    sql = '''SELECT COUNT(id_velo) AS nbr_velos FROM velo'''
    mycursor.execute(sql)
    nbr_velos = mycursor.fetchall()

    sql = '''SELECT id_type_velo, libelle_type_velo, COUNT(id_velo) AS nbr_velos
             FROM type_velo
             LEFT JOIN velo ON type_velo.id_type_velo = velo.type_velo_id
             GROUP BY id_type_velo, libelle_type_velo;'''
    mycursor.execute(sql)
    types_velos_nb = mycursor.fetchall()

    sql = '''SELECT id_type_velo, libelle_type_velo, SUM(stock * prix_declinaison) AS cout_total
             FROM type_velo
             LEFT JOIN velo ON type_velo.id_type_velo = velo.type_velo_id
             LEFT JOIN declinaison_velo ON velo.id_velo = declinaison_velo.velo_id
             GROUP BY id_type_velo, libelle_type_velo;'''
    mycursor.execute(sql)
    datas_show1 = mycursor.fetchall()

    sql = '''SELECT id_velo, nom_velo, COUNT(id_declinaison_velo) AS nbr_declinaisons_velos
             FROM velo
             LEFT JOIN declinaison_velo ON velo.id_velo = declinaison_velo.velo_id
             GROUP BY id_velo, nom_velo;'''
    mycursor.execute(sql)
    datas_show2 = mycursor.fetchall()

    labels1 = [row['libelle_type_velo'] for row in datas_show1]
    values1 = [float(row['cout_total']) for row in datas_show1]

    labels2 = [row['nom_velo'] for row in datas_show2]
    values2 = [float(row['nbr_declinaisons_velos']) for row in datas_show2]

    return render_template('admin/dataviz/dataviz_etat_1.html', nbr_velos=nbr_velos, labels1=labels1, values1=values1, types_velos_nb=types_velos_nb, labels2=labels2, values2=values2)

# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    # mycursor = get_db().cursor()
    # sql = '''    '''
    # mycursor.execute(sql)
    # adresses = mycursor.fetchall()

    # exemples de tableau "résultat" de la requête
    adresses = [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    # recherche de la valeur maxi "nombre" dans les départements
    # maxAddress = 0
    # for element in adresses:
    #     if element['nbr_dept'] > maxAddress:
    #         maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    # if maxAddress != 0:
    #     for element in adresses:
    #         indice = element['nbr_dept'] / maxAddress
    #         element['indice'] = round(indice,2)

    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html', adresses=adresses)
