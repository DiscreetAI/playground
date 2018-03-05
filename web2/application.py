from flask import Flask, render_template, request, redirect, url_for, Response, json, jsonify
# from flask import session
# from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import requests
import pandas as pd
from collections import defaultdict
from pandas.io.sql import SQLTable
import datetime
import base64
import os

application = Flask(__name__)
application.config['DEBUG'] = True
# SESSION_TYPE = 'redis'
application.config.from_object(__name__)
# Session(application)
POSTGRES = {
    'user': 'datashark',
    'pw': 'datashark',
    'db': 'datasharkdb',
    'host': 'datasharkdatabase.cwnzqu4zi2kl.us-west-1.rds.amazonaws.com',
    'port': '5432'
}
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
application.requests_session = requests.Session()
application.secret_key = os.urandom(24)
db = SQLAlchemy(application)