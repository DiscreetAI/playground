POSTGRES = {
	'user': 'datashark',
	'pw': 'datashark',
	'db': 'datasharkdb',
	'host':  'datasharkdatabase.cwnzqu4zi2kl.us-west-1.rds.amazonaws.com',
	'port': '5432'
}
DBString = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db = SQLAlchemy(DBString)