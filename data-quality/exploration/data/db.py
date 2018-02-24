from flask import Flask
from flask_sqlalchemy import SQLAlchemy

POSTGRES = {
	'user': 'datashark',
	'pw': 'datashark',
	'db': 'datasharkdb',
	'host':  'datasharkdatabase.cwnzqu4zi2kl.us-west-1.rds.amazonaws.com',
	'port': '5432'
}
DBString = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# print(DBString)
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DBString
# db = SQLAlchemy(app)
#
# print(db)


from sqlalchemy import create_engine
engine = create_engine(DBString)

from sqlalchemy import inspect
inspector = inspect(engine)

for table_name in inspector.get_table_names():
	print("Table: %s" % table_name)
	for column in inspector.get_columns(table_name):
		print("Column: %s" % column['name'])
