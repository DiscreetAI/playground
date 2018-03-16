from application import *

@application.route('/get/Fitbit', methods = ['POST', 'GET'])
def get_fitbit():
    code = request.args.get('code')
    user_id = request.args.get('state')
    print('got code')
    print(code)
    client_id = '22CH8Y'
    client_secret = '92ef15bf527e8c3684ff6f54517d235e'
    encoded = base64.b64encode(
        "{}:{}".format(
            client_id,
            client_secret
        ).encode('utf-8')
    ).decode('utf-8')
    print('encoded')
    print(encoded)
    encode64 = 'MjJDSDhZOjkyZWYxNWJmNTI3ZThjMzY4NGZmNmY1NDUxN2QyMzVl'
    encoded = encode64
    header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic {}'.format(encoded)
        }
    r = requests.post(
        get_auth_url(code),
        headers=header
    )
    response = r.json()
    response2 = json.loads(r.text)
    print('Access token')
    print(response2)
    requests.post('https://demo.dataagora.com/insert/Fitbit', data = {'accessToken':response2['access_token'], 'uid':user_id})
    return render_template('payment.html') #change this!

def get_auth_url(code):
    redirect_uri = 'https://demo.dataagora.com/get/Fitbit'
    return 'https://api.fitbit.com/oauth2/token?code={code}&client_id={client_id}&grant_type=authorization_code&redirect_uri={redirect}'.format(
        code=code,
        client_id='22CH8Y',
        redirect = redirect_uri
    )

@application.route('/oauth/Fitbit', methods = ['POST', 'GET'])
def fitbit_oauth():
    user_id = '' #GEORGY: pass in user id however you want, and fill in this variable
    if 'scopes' in request.form:
        scopes = request.form['scopes']
    else:
        scopes = ['activity', 'nutrition', 'heartrate', 'location', 'profile', 'sleep', 'settings', 'weight']
    url = 'https://www.fitbit.com/oauth2/authorize?client_id=22CH8Y&prompt=none&redirect_uri=https://demo.dataagora.com/get/Fitbit&response_type=code&state={}&scope='.format(user_id)
    for scope in scopes:
        url += scope + '%20'
    url = url[:-3]
    return redirect(url)