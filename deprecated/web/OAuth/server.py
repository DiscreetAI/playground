## FOR DATASHARK
# client_id = '228MWM'
# client_secret = '699ed916a01faff2cb3139f437b897f1'


## FOR SPECIFIC USER - ROHAN - CONFIDENTIAL
accesstoken = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1U1pMN0YiLCJhdWQiOiIyMjhNV00iLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNTEwMjExODg2LCJpYXQiOjE1MTAxMjU0ODZ9.LfbHvsGw7N1n2KfxnT6Q0xNtkiPOQJQ1zA9Nj3Xquw0'
# refresh_token = 'bbb44b3a0e05a4235b9bd837481d4796372ee3d51d5a1f4b2b82af4c85216534'


import requests
import json
import pandas as pd
from collections import defaultdict

def fitbit_data(access_token=accesstoken):
	header = {'Authorization': 'Bearer ' + access_token}


	## FOR FITBIT DAILY ACTIVITY SUMMARY

	fitbit_daily_activity_summary_values = ['lightlyActiveMinutes', 'caloriesBMR', 'caloriesOut', 'marginalCalories', 'fairlyActiveMinutes', 'veryActiveMinutes', 'sedentaryMinutes', 'restingHeartRate', 'elevation', 'activityCalories', 'activeScore', 'floors', 'steps']
	fitbit_daily_activity_summary_endpoint = 'https://api.fitbit.com/1/user/-/activities/date/2017-9-{0}.json'

	dict = defaultdict(lambda: [])

	for date in range(1, 30):
		endpoint = fitbit_daily_activity_summary_endpoint.format(str(date).zfill(2))
		# print(endpoint)
		response = requests.get(endpoint, headers=header)
		parsed = json.loads(response.text)

		# print(date)
		for value in fitbit_daily_activity_summary_values:
			if value in parsed['summary']:
				dict[value].append(parsed['summary'][value])
			else:
				dict[value].append(None)
		if 'distances' in parsed['summary']:
			distances = parsed['summary']['distances']
			if len(distances) > 0:
				if 'distance' in distances[0]:
					dict['distance'].append(distances[0]['distance'])
	fitbit_daily_activity_summary_df = pd.DataFrame(dict)
	return fitbit_daily_activity_summary_df
