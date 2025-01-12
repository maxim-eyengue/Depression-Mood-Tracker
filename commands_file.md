![ML Zoomcamp Illustration](https://github.com/maxim-eyengue/Python-Codes/blob/main/ML_Zoomcamp_2024/zoomcamp.jpg)

# Commands used for the Capstone Project

## Setting up the environment
### To create the environment used for our project:
```bash
conda create -n ml-zoomcamp python=3.11
```

### To activate it:
```bash
conda activate ml-zoomcamp
```

### To install some libraries:
```bash
conda install numpy pandas scikit-learn seaborn jupyter
```

### To deactivate the environment after completing the project:
```bash
conda deactivate
```


## Managing scripts
### To convert a jupyter notebook to a script:
```bash
jupyter nbconvert --to script capstone_project_01.ipynb
```

### To rename a script:
```bash
mv capstone_project_01.py train.py
```


## Managing dependencies with pipenv
### Install pipenv:
```bash
pip install pipenv
```

### Set up the pip environment:
```bash
pipenv install flask scikit-learn==1.5.1 gunicorn
```

### Create and activate the environment so we can run code:
```bash
pipenv shell
```

### Run a command directly directly in a pipenv ennvironment:
```bash
pipenv run `add the command to execute`
```


## For managing the docker image
### Create a Docker image for the project:
```bash
docker build -t depression-mood-tracker .
```

### Visualize available Docker images:
```bash
docker images
```

### Run the Docker image container:
```bash
docker run -it --rm -p 9696:9696 depression-mood-tracker
```

## For AWS Elastic Beanstalk deployment
### To install AWS Elastic Beanstalk in our environment as a development dependency:
```bash
pipenv install awsebcli --dev
```

### Alert: For the following commands, first activate the environment  with `pipenv shell`.

### To initialize the application with AWS Elastic Beanstalk using a Docker image:
```bash
eb init -p "Docker running on 64bit Amazon Linux 2" depression-mood-tracker -r us-east-1 
```

### To deploy the application locally:
```bash
eb local run --port 9696
```

### To deploy the application to the cloud:
```bash
eb create depression-mood-tracker-env
```

### To terminate the Elastic Beanstalk environment:
```bash
eb terminate depression-mood-tracker-env
```


## Running the web service
### To run the flask application with gunicorn:
```bash
gunicorn --bind 0.0.0.0:9696 predict:app
```

### To run the flask application locally with the pipenv environment:
```bash
pipenv run gunicorn --bind 0.0.0.0:9696 predict:app
```

### Run the Docker container containing the web service:
```bash
docker run -it --rm -p 9696:9696 depression-mood-tracker
```


## Testing the service
### Before deploying as a flask application:
```bash
python no_app_predict_test.py
```

### Testing the flask application with gunicorn, or locally with the pipenv environment, or locally with the docker image, or locally with Elastic Beanstalk:
```bash
python predict_test.py
```

### Testing the application after deployement to the cloud with AWS elastic Beanstalk:
```bash
python predict_test_cloud.py
```

---