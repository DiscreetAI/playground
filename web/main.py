from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
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
    db.session.execute('create table test(name text)')
    db.session.commit()
    return render_template('index.html')


@application.route('/results', methods=['POST'])
def results():
    categ = request.form['categ']
    # insert = Test(name=categ)
    # db.session.add(insert)
    # db.session.commit()
    db.session.execute('insert into test values(:val)', {'val': categ})
    db.session.commit()
    result = db.session.execute('select * from test')
    db.session.commit()
    r = result.first()
    return render_template('left-sidebar.html', cat = r)

if __name__ == "__main__":
    application.run()
