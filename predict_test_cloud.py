### Depression Mood Tracker ###

# import necessary library
import requests

# host and url address for making predictions
host = "add the address provided by Elastic Beanstalk"
url = f'http://{host}/predict'

# New patient information
patient = {'age': 24,
           'marital_status': 'single',
           'education_level': 'masters_degree',
           'number_of_children': 0,
           'smoking_status': 'non_smoker',
           'physical_activity_level': 'moderate',
           'employment_status': 'unemployed',
           'alcohol_consumption': 'low',
           'dietary_habits': 'moderate',
           'sleep_patterns': 'poor',
           'history_of_mental_illness': 'no',
           'history_of_substance_abuse': 'yes',
           'family_history_of_depression': 'yes',
           'log_income': 1.59}

# send a request for making predictions
response = requests.post(url, json = patient).json()
# Print the response
print(response)

# Define a treatment if necessary
if response['depression_mood']:
    print('Define a treatment for the patient tested.')
else:
    print('The patient seems healthy: no treatment needed.')
    
# ---