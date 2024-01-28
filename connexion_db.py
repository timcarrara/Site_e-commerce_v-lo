from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

import os
from dotenv import load_dotenv
load_dotenv('./data.env')


def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host=os.environ.get("HOST"),                # à modifier
            user=os.environ.get("LOGIN"),               # à modifier
            password=os.environ.get("PASSWORD"),        # à modifier
            database=os.environ.get("DATABASE"),        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db
