from application import *

@application.route('/oauth/Uber', methods = ['POST', 'GET'])
def uber_oauth():
    return redirect('https://login.uber.com/oauth/v2/authorize?client_id=cvcaMdUYPlqkoFtrEECV1bbEEBnmpd5K&scope=profile%20history%20places&response_type=code&redirect_uri=https://demo.dataagora.com/get/Uber') 

@application.route('/get/Uber', methods = ['POST', 'GET'])
def get_uber():
    code = request.args.get('code')
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
    return render_template('payment.html')