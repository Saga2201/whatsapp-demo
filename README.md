# Whatsapp Integration

### Clone the repo
```
git clone git@github.com:Saga2201/whatsapp-demo.git
```

## 1. Run app locally

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirement.txt.

### Make virtual environment
```bash
python3 -m venv venv
```

### Activate virtual environment
```bash
source venv/bin/activate  
```

### Install requirements
```bash
pip install -r requirements.txt
```

### ENV

```
AZURE_ENDPOINT=https://project.openai.azure.com/
AZURE_API_KEY=8******************18
DEPLOYMENT_NAME=model_name
```

### Run the BE
```bash
python manage.py runserver
```

## 2. Run app using docker

### Build the image
```bash
docker build -t whatsapp-django .
```

### run 
```bash
docker run -d -p 8000:8000 whatsapp-django 
```

### check app
```bash
docker ps
```

## Postman collection
```
https://documenter.getpostman.com/view/25481132/2sAYJ1kMkL
```
