from application import *

@application.route('/get/Fitbit', methods = ['POST', 'GET'])
def getFitbit():
    code = request.args.get('code')
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
    return render_template('payment.html')

def get_auth_url(code):
    redirect_uri = 'https://demo.dataagora.com/get/Fitbit'
    return 'https://api.fitbit.com/oauth2/token?code={code}&client_id={client_id}&grant_type=authorization_code&redirect_uri={redirect}'.format(
        code=code,
        client_id='22CH8Y',
        redirect = redirect_uri
    )

@application.route('/oauth/Fitbit', methods = ['POST', 'GET'])
def fitbitOAuth():
    return redirect('https://www.fitbit.com/oauth2/authorize?client_id=22CH8Y&prompt=none&redirect_uri=https://demo.dataagora.com/get/Fitbit&response_type=code&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight&state=true')