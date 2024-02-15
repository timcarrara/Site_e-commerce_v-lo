from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/Site_e-commerce_velo')
load_dotenv(os.path.join(project_folder, '.env'))

def get_db():
    db = getattr(g, '_database', None)
    if 'db' not in g:
        g.db = pymysql.connect(
            host=os.environ.get("HOST"),
            user=os.environ.get("LOGIN"),
            password=os.environ.get("PASSWORD"),
            database=os.environ.get("DATABASE"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db