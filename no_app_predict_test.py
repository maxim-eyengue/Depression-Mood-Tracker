#!/usr/bin/env python
# coding: utf-8

####### Test the depression tracker without any application #######

#### Necessary import
import pickle # to manipulate models

### Load the model
# Name of the model
input_file = 'dt_model_depth_3_min_samples_leaf_500.bin'

# Open file to read it
with open(input_file, 'rb') as f_in:
    # Load the model
    One_Hot_encoder, dt = pickle.load(f_in)


### Test the model
# Random patient information
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
# Format input data
X_i = One_Hot_encoder.transform([patient])
# Make soft predictions
y_i_pred = round(dt.predict_proba(X_i)[0, 1], 3)

# Print customer info and the model's prediction
print('input data:', patient)
print('Depression probability:', y_i_pred)
# Define a treatment if necessary
if y_i_pred >= 0.5:
    print('Define a treatment for the patient-test.')

# ---