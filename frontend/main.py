from flask import Flask, render_template, request, redirect, url_for, Response, json
from flask_sqlalchemy import SQLAlchemy
import requests
import pandas as pd
from collections import defaultdict
from oauth import *
from adapters import  *
# import OAuth.spotify
# import OAuth.youtube1
# import OAuth.twitter

#from models import db
# import sys
# serverpath = "/OAuth/server"
# if not serverpath in sys.path:
#     sys.path.insert(0, serverpath)
#
# from OAuth.server import fitbit_data



@application.route("/", methods=['GET', 'POST'])
def main():
    return render_template('homepage.html')

@application.route("/decide", methods=['GET', 'POST'])
def decide():
    print(request.form['decide'])
    if request.form['decide'] == 'buy':
        return redirect('/buy')
    else:
        return redirect('/sell')

@application.route("/sell", methods=['GET', 'POST'])
def sell():
    return render_template('sellapi.html')
@application.route("/buy", methods=['GET', 'POST'])
def buy():
    return render_template('buyapi.html')
@application.route("/home", methods=['POST'])
def home():
    return redirect('/')

@application.route("/sellwhat", methods=['POST'])
def redirectOAuth():
    if 'sell' in request.form:
        categ = request.form['sell']
    else:
        categ = 'lol'
    #return execute()
    #insert_fitbit()
    if categ == 'Fitbit':
        return fitbit_oauth()
    elif categ == 'Uber':
        return uber_oauth()
    elif categ == 'Lyft':
        return lyft_oauth()
    elif categ == 'Twitter':
        return twitter_oauth()
    elif categ == 'Spotify':
        return spotify_oauth()
    else:
        return render_template('sellapi.html')

@application.route("/buyapi", methods=['POST'])
def redirectAPI():
    if 'buy' in request.form:
        categ = request.form['buy']
    else:
        categ = 'lol'
    
    table_name = "fitbit_daily_activity_summary"
    col_names = get_columns(table_name)
    temp = str(col_names)
    #print(temp)
    temp = temp.replace("'", '"')
    # print(temp)
    import ast
    col_names = ast.literal_eval(temp)
    maxUsers = -1
    api = ''
    logo = ''
    template = ''
    def capAndSpace(string):
        return ' '.join(list(string.upper()))
    if 'buy' in request.form:
        print("yes")
        if request.form['buy'] == 'Fitbit':
            maxUsers = get_user_count('user_id', 'fb_activities')
            print(maxUsers)
        api = capAndSpace(request.form['buy'])
        template = url_for('static',filename='images/' + request.form['buy'].lower() + '.png')

    print(template, "sup")
    return render_template('left-sidebar.html', table=table_name, cols=json.dumps(col_names), users=maxUsers, api=api, logo=template)


@application.route('/results', methods=['POST'])
def results():
    if 'test' in request.form:
        categ = request.form['test']
    else:
        categ = 'lol'
    #return execute()
    #insert_fitbit()
    if categ == 'Fitbit':
        return fitbit_oauth()
    elif categ == 'Uber':
        return uber_oauth()
    elif categ == 'Lyft':
        return lyft_oauth()
    elif categ == 'Twitter':
        return twitter_oauth()
    elif categ == 'Spotify':
        return spotify_oauth()
    table_name = "fitbit_daily_activity_summary"
    col_names = get_columns(table_name)
    temp = str(col_names)
    #print(temp)
    temp = temp.replace("'", '"')
    # print(temp)
    import ast
    col_names = ast.literal_eval(temp)
    maxUsers = -1
    api = ''
    logo = ''
    template = ''
    def capAndSpace(string):
        return ' '.join(list(string.upper()))
    if 'categ' in request.form:
        print("yes")
        if request.form['categ'] == 'Fitbit':
            maxUsers = get_user_count('user_id', 'fb_activities')
            print(maxUsers)
        api = capAndSpace(request.form['categ'])
        template = url_for('static',filename='images/' + request.form['categ'].lower() + '.png')

    # print(col_names)
    return render_template('left-sidebar.html', table=table_name, cols=json.dumps(col_names), users=maxUsers, api=api, logo=template)

def get_table(tableName):
    query = "select * from {};".format(tableName)
    df = pd.read_sql_query(query, db.engine)
    return df 

def get_user_count(colName, tableName):
    query = "select count(distinct {col_name}) as count from {table_name};".format(col_name=colName, table_name=tableName)
    df = pd.read_sql_query(query, db.engine)
    return df['count'][0] 

#userDF is dataframe of userids with corresponding metadata.
#dfArr is array of tuples (dataframe, api) to be filtered
def fake_filter(userInfo, dfArr, minAge=0, maxAge=200, city=None, gender=None):
    filtereDFs = []
    for df, api in dfArr:
        if not hasAge[api]:
            tempUser = userInfo[userInfo['age'] != None]
            merged = pd.merge(df, userInfo, left_on=idNames[api], right_on='userid', how='inner')
            merged = merged[df.columns + ['age']]
            df = merged
        df = df[df['age'] > minAge]
        df = df[df['age'] < maxAge]
        if not hasCity[api]:
            tempUser = userInfo[userInfo['city'] != None]
            merged = pd.merge(df, userInfo, left_on=idNames[api], right_on='userid', how='inner')
            merged = merged[df.columns + ['city']]
            df = merged
        if city != None:
            df = df[df['city'] == city]
        if not hasGender[api]:
            tempUser = userInfo[userInfo['gender'] != None]
            merged = pd.merge(df, userInfo, left_on=idNames[api], right_on='userid', how='inner')
            merged = merged[df.columns + ['gender']]
            df = merged
            if gender != None:
                df = df[df['gender'] == gender]
        filtereDFs.append(df)
    return filteredDFs

#Assume given a dataframe where for each user, there is 1 for each API if user has data from API (0 otherwise), and demographic information.
def count(userInfo, api):
    return userInfo[userInfo['age'] != None & userInfo['city'] != None & userInfo['gender'] != None & userInfo['city'] != None & userInfo[api] == 1]        
        
    
@application.route('/checkout', methods=['POST'])
def checkout():
    return render_template('checkout.html')


@application.route('/account', methods=['POST'])
def account():
    return render_template('account.html')


@application.route('/payment', methods=['POST'])
def payment():
    return render_template('payment.html')




@application.route('/execute', methods=['POST'])
def execute():
    print("execute called")
    #query = request.form['query']
    #print(query)
    #df = pd.read_sql_query(query, db.engine)
    df = pd.read_sql_query("select * from fitbit_daily_activity_summary", db.engine)
    csv = df.to_csv(index=False)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=fitbit.csv"}
        )






def get_columns(categ):
    cmd = 'select col, description from metadata where table_name=:val'
    result = db.session.execute(cmd, {'val': categ})
    db.session.commit()
    return result.fetchall()

if __name__ == "__main__":
    application.run()
