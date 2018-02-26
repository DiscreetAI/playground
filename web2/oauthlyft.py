from application import *

@application.route('/oauth/Lyft', methods = ['POST', 'GET'])
def lyft_oauth():
    return redirect('https://api.lyft.com/oauth/authorize?client_id={client_id}&scope=public%20profile%20rides.read%20rides.request%20offline&state=true&response_type=code'.format(client_id='xWcQoJgCDyyx')) 

@application.route('/get/Lyft', methods = ['POST', 'GET'])
def get_lyft():
    code = request.args.get('code')
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
    return render_template('payment.html')