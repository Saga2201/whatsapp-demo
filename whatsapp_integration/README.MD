# Whatsapp Integration

### Clone the repo
```
url
```

## 1. Run app locally

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirement.txt.

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
```
python manage.py runserver
```

## 2. Run app using docker

### Build the image
```
docker build -t whatsapp-django .
```

### run 
```
docker run -d -p 8000:8000 whatsapp-django 
```

### check app
```
docker ps
```

## Postman collection
```
https://documenter.getpostman.com/view/25481132/2sAYJ1kMkL
```
