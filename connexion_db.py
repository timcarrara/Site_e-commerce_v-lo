from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

def get_db():
    db = getattr(g, '_database', None)
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",  # "serveurmysql" sur les machines de l'IUT
            user="SAE_commun",
            password="123456789",
            database="e_commerce",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db