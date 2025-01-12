#!/usr/bin/env python
# coding: utf-8

####### Depression Mood Tracker #######
# The goal of this project is to assess depression in patients by analyzing personal and lifestyle factors. 

#### Necessary import
import pickle # to manipulate models
import numpy as np # for matrices and numerical manipulations
import pandas as pd # for dataframes
from sklearn.feature_extraction import DictVectorizer # for One-Hot Encoding
from sklearn.model_selection import train_test_split, KFold # for cross-validation techniques
from sklearn.tree import DecisionTreeClassifier # for decision trees

# Libraries versions
print("pandas version:", pd.__version__)
print("numpy version:", np.__version__)

#### Parameters
print("Setting parameters")
# Optimal model's hyperparameters values
max_depth, min_samples_leaf = 3, 500
# Number of splits for Kfold Cross-Validation
n_splits = 5
# Model file name
output_file = f'dt_model_depth_{max_depth}_min_samples_leaf_{min_samples_leaf}.bin'

#### Read the dataframe
df = pd.read_csv("data/depression_data.csv")

#### Data Preparation
print("Preparing Data")
### Data Ethics and feature normalisation
# Normalisation of column names
df.columns = df.columns.str.lower().str.replace(' ', '_')
# Drop patient names
df.drop(columns = "name", inplace = True)

### Down-sampling data
# Get the minority class size
down_size = len(df[df.chronic_medical_conditions == "Yes"])
# Get a down-sampled subset of the majority class
df_maj_class = df[df.chronic_medical_conditions == "No"].sample(n = down_size, random_state = 37)
# Build the balanced dataset
bal_df = pd.concat([df_maj_class, # majority class
                    df[df.chronic_medical_conditions == "Yes"] # minority class
                   ])
# Let's shuffle the data-set
bal_df = bal_df.sample(frac = 1, random_state = 1).reset_index(drop = True)

### Dropping outliers
# Get 10th (low) and 90th (high) percentile
low, high = bal_df["income"].quantile([0.1, 0.9])
# Remove outliers by income
bal_df = bal_df[bal_df["income"].between(low, high)]

### Feature engineering
# Income feature engineering
bal_df["log_income"] = np.log1p(bal_df.income)
# Delete the previous income variable
del bal_df["income"]

### Storing features by type
# list of categorical feature variables
numerical = bal_df.select_dtypes("number").columns.to_list()
# list of categorical feature variables
categorical = bal_df.drop(columns = "chronic_medical_conditions").select_dtypes("object").columns.to_list()

### String normalisation
# For each categorical variable
for cat in categorical:
    # Format string values
    bal_df[cat] = (bal_df[cat].
                   str.lower().
                   str.replace(" ", "_").
                   str.replace("'", "").
                   str.replace("-", "_"))

### Target Variable encoding
bal_df["chronic_medical_conditions"] = (bal_df["chronic_medical_conditions"] == "Yes").astype(int)


#### Data Splitting into Train - Validation - Test
print("Data splitting")
# Splitting into full train and test
df_full_train, df_test = train_test_split(bal_df, test_size = 0.2, random_state = 42)
# Splitting into train and test
df_train, df_val = train_test_split(df_full_train, test_size = 0.25, random_state = 42)
# Reset indexes
df_train = df_train.reset_index(drop = True)
df_test = df_test.reset_index(drop = True)
df_val = df_val.reset_index(drop = True)
# Get the target values
y_train = df_train.chronic_medical_conditions.values
y_test = df_test.chronic_medical_conditions.values
y_val = df_val.chronic_medical_conditions.values
# Drop the target from our data sets
del df_train["chronic_medical_conditions"]
del df_test["chronic_medical_conditions"]
del df_val["chronic_medical_conditions"]


#### Model Building
print("Model building")

### Functions for training the model and making inference
# Function for training a random forest classifier
def train(df_train, y_train, max_depth = 3, min_samples_leaf = 500):
    """
    This function takes in a training data set, and its target variable, with hyperparameters
    of a decision tree classifier and trains the model, to return the encoder
    and the classifier trained.
    ---
    df_train: Training data set
    y_train: Training target variable
    max_depth: Maximum depth of decision tree classifier,
                    default: 3
    min_samples_leaf: Minimum sample leaves for decision tree classifier,
                    default: 500
    """
    # Convert training set to list of dictionaries
    train_dicts = df_train[categorical + numerical].to_dict(orient = 'records')
    
    # Initialize One-Hot-Encoder (vectorizer)
    One_Hot_encoder = DictVectorizer(sparse = True)
    # One-Hot-Encoder training and train data encoding
    X_train = One_Hot_encoder.fit_transform(train_dicts)

    # Initialize decision tree model
    dt = DecisionTreeClassifier(max_depth = max_depth,
                                min_samples_leaf = min_samples_leaf,
                                random_state = 42)
    
    # Model training
    dt.fit(X_train, y_train)

    # return one-hot-encoder and decision tree model
    return One_Hot_encoder, dt

# Function to make predictions with a random forest classifier
def predict(df, One_Hot_encoder, dt):
    """
    This function takes in a dataframe, a One-Hot-Encoder (dict vectorizer), and
    a decision tree model already trained in order to make predictions.
    ---
    df: dataframe to evaluate the model
    One_Hot_Encoder: dict vectorixer to encode categorical variables in the test dataframe
    rf: decision tree classifier already trained
    """
     # Convert data to list of dictionaries
    dicts = df[categorical + numerical].to_dict(orient = 'records')

    # One-Hot-Encoding
    X = One_Hot_encoder.transform(dicts)
    # Make predictions
    y_pred = dt.predict(X)
    
    # return predictions
    return y_pred

### Cross - Validation Training
print("Performing KFold Cross-Validation")
# Kfold cross-validation initalization
kfold = KFold(n_splits = n_splits, shuffle = True, random_state = 1)
# Initialize scores
scores = []
# Initialize number of folds
fold = 0
# For each iteration of K-fold split and the pair of indexes generated
for train_idx, val_idx in kfold.split(df_full_train):
    # Select train and validation data
    df_train = df_full_train.iloc[train_idx]
    df_val = df_full_train.iloc[val_idx]

    # Select target variables
    y_train = df_train.chronic_medical_conditions.values
    y_val = df_val.chronic_medical_conditions.values

    # Train model
    One_Hot_encoder, dt = train(df_train, y_train)
    # Make predictions
    y_pred = predict(df_val, One_Hot_encoder, dt)

    # Get score
    acc = round(100 * (y_pred == y_val).mean(), 2)
    # Store score
    scores.append(acc)
    # print auc
    print(f"Accuracy on fold {fold} is {acc} %.")

    # Increment number of fold
    fold += 1
    
# Print scores' means and standard deviations
print("Validation results:")
print('acc mean = %.2f, acc std = +- %.2f' % (np.mean(scores), np.std(scores)))

### Final Model Training
print("Final model training")
# Optimal decision tree model training
One_Hot_encoder, dt = train(df_full_train[categorical + numerical], df_full_train.chronic_medical_conditions,
                            max_depth = max_depth, min_samples_leaf = min_samples_leaf)
# Make predictions
y_pred = predict(df_test, One_Hot_encoder, dt)
# accuracy score
print('Optimal model accuracy = %.2f.' % (100 * (y_pred == y_test).mean()))

### Save the model
# Open file and write into it
with open(output_file, 'wb') as f_out: 
    # Save model
    print("Storing the model into a file:")
    pickle.dump((One_Hot_encoder, dt), f_out)
    
print(f"The model is saved to {output_file}.")

# ---