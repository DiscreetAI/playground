from application import *

@application.route('/oauth/Lyft', methods = ['POST', 'GET'])
def lyft_oauth():
    session_token = '' #GEORGY: pass in session_token however you want, and fill in this variable
    if 'scopes' in request.form:
        scopes = request.form['scopes']
    else:
        scopes = ['public', 'profile', 'rides.read', 'rides.request']
    url = 'https://api.lyft.com/oauth/authorize?client_id={client_id}&response_type=code&state={state}&scope='.format(client_id='xWcQoJgCDyyx', state=session_token)
    for scope in scopes:
        url += scope + '%20'
    url = url[:-3]
    return redirect(url) 

@application.route('/get/Lyft', methods = ['POST', 'GET'])
def get_lyft():
    code = request.args.get('code')
    session_token = request.args.get('state')
    print('got code')
    print(code)
    client_id = 'xWcQoJgCDyyx'
    client_secret = 've3ul8VMMiiQ7zrft33S2gzAy8258436'
    params = {
        'code': code,
        'grant_type': 'authorization_code',
    }
    user = {client_id:client_secret}
    encoded = base64.b64encode(
        "{}:{}".format(
            client_id,
            client_secret
        ).encode('utf-8')
    ).decode('utf-8')
    print('encoded')
    print(encoded)
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic {}'.format(encoded), 
    }
    response = requests.post(
        'https://api.lyft.com/oauth/token',
        headers=header,
        data = params
    )
   
    r = json.loads(response.text)
    print('Access token')
    print(r)
    requests.post('https://demo.dataagora.com/insert/Lyft', data = {'accessToken':r['access_token'], 'uid': session_token})
    return render_template('payment.html')