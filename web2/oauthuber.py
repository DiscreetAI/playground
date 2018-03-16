from application import *

@application.route('/oauth/Uber', methods = ['POST', 'GET'])
def uber_oauth():
    user_id = '' #GEORGY: pass in user id however you want, and fill in this variable
    url = 'https://login.uber.com/oauth/v2/authorize?client_id={client}&response_type=code&redirect_uri={redirect}&state={state}&scope='.format(client = 'cvcaMdUYPlqkoFtrEECV1bbEEBnmpd5K', redirect = 'https://demo.dataagora.com/get/Uber', state = user_id)
    if 'scopes' in request.form:
        scopes = request.form['scopes']
    else:
        scopes = ['profile', 'history', 'places']
    for scope in scopes:
        url += scope + '%20'
    url = url[:-3]
    return redirect(url) 

@application.route('/get/Uber', methods = ['POST', 'GET'])
def get_uber():
    code = request.args.get('code')
    user_id = request.args.get('state')
    print('got code')
    print(code)
    client_id = 'cvcaMdUYPlqkoFtrEECV1bbEEBnmpd5K'
    client_secret = 'J7vY3yBGZr19EIrtibQZPhJm2qPulKy-Zs2VMMQz'
    params = {
        'client_id': client_id, 
        'client_secret': client_secret,
        'redirect_uri': 'https://demo.dataagora.com/get/Uber',
        'code': code,
        'grant_type': 'authorization_code',
    }
    header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    response = requests.post(
        'https://login.uber.com/oauth/v2/token',
        data=params,
        headers=header
    )
   
    r = json.loads(response.text)
    print('Access token')
    print(r)
    requests.post('https://demo.dataagora.com/insert/Uber', data={'accessToken': r['access_token'], 'uid':user_id})
    return render_template('payment.html')