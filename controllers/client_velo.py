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
    #list_param = []
    #condition_and = ""
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