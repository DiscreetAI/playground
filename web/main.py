from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
#from models import db

db = SQLAlchemy()

application = Flask(__name__)
application.config['DEBUG'] = True

POSTGRES = {
    'user': 'datashark',
    'pw': 'datashark',
    'db': 'datasharkdb',
    'host':  'datashark-database.cwnzqu4zi2kl.us-west-1.rds.amazonaws.com',
    'port': '5432'
}
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_application(application)


@application.route("/")
def main():
    return render_template('index.html')


@application.route('/results', methods=['POST'])
def results():
    categ = request.form['categ']
    col_names = get_columns(categ)
    return render_template('left-sidebar.html', cat = categ)

@application.route('/execute')
def execute(query):
    df = pandas(query, db.session)
    csv = df.to_csv()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=data.csv"}
        )

def get_columns(categ):
    cmd = 'select col, description from metadata where table_name==:val'
    result = db.session.execute(text(cmd), val=categ)
    db.session.commit()
    return result.fetchall()

if __name__ == "__main__":
    application.run()
