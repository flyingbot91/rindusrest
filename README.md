# Rindus demo API 

A simple REST API with dummy data from [JSONPlaceholder](https://jsonplaceholder.typicode.com).

## Required libraries
- `Django`: Python web framework.
- `djangorestframework`: Python web framework for REST web APIs.
- `requests`: Used to handle HTTP requests/responses.
- `psycopg2-binary`: PostgreSQL database adapter for python.
- `python-dotenv`: Used to load sensitive information from .env files.
- `black`: Code formatter.
- `coverage`: Code coverage measurement for python.
- `pylint`: Python code static checker.

## Setup

### Development
```
# Install required packages (tested on Ubuntu systems)
sudo apt-get install git postgresql postgresql-contrib

# Clone the repository
git clone https://github.com/flyingbot91/rindusrest.git

# Create the virtual environment and install required packages
cd rindusrest 
python -m venv env
source env/bin/activate
env/bin/python -m pip install --upgrade pip
env/bin/python -m pip install -r requirements/development.txt

# Get .env file
cp .env-files/development .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Ingest data
python manage.py import_data

# Run server
python manage.py runserver 0.0.0.0:8000

# Create the Django superuser
python manage.py createsuperuser
```

#### Testing
```
# Unittests & coverage
coverage run manage.py test api
coverage report --skip-covered
```

### Production
The configuration data has been split in the files under the folder **./env-files/**.

These files contain demo values, but feel free to modify them according to your needs.

**NOTE:** Migrations and data synchronization (data import) handled automatically during the build process.

1. Clone the repository
```
git clone https://github.com/flyingbot91/rindusrest.git
```
2. Modify the files under **./env-files/** (not required for testing purposes):

3. Build the project
```
docker-compose -f docker-compose.yml up -d --build
```
4. Create a Django superuser
```
docker-compose -f docker-compose.yml exec app python manage.py createsuperuser
```

## How to run 

In order to test the application you can use [curl](https://curl.se/docs/manpage.html). For example:

```
# Get token
curl -F username=<username> -F password=<password> http://localhost:8000/api/auth-token/
# Get comment
curl -v -H "Accept: application/json" -H "Authorization: Bearer {token}" http://127.0.0.1:8000/api/comments/<comment_id>/
```

## Logging

Data ingestion logs can be found at **/tmp/rindus.log**.
