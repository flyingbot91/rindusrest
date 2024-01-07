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

## System synchronization (not implemented):

Hereby I propose different synchronization strategies:

1. **Pull-based sync**: Periodically pull data from the remote API and update the local API accordingly. This can be done using scheduled jobs or triggers.
2. **Push-based sync**: Define triggers in the local API to push updates to the remote API whenever changes occur. This could involve event-based mechanisms or webhooks.
3. **Two-way sync**: Sync data in both directions. This way, changes made in one API are reflected in the other.

Since we are using our REST API system as MASTER, **we must go with option 2 (push-based)** because options **1 and 3 rely on an external system which is not managed by us**.

In order to push data from MASTER we have different approaches:

1. The simplest proposal is to use **cron jobs**. Not recommended for many reasons:
	* When the cron job is triggered it should look for objects created/updated/deleted in the API during the actual time window. As the number of objects in the database grow the query time will do so.
	* It is not scalable and does not respond to request peaks because if the sync process is not completed during the current time window it will overlap with the next one. Hence, the API may overload and underperform.

2. Use of a queueing system (RabbitMQ + Celery, Redis + Celery, etc.).
    * This system can keep ordered sets of events which allows us to scale the system depending on our requirements.
    * Additionally it includes the possibility to add task retries, enqueue failed tasks, etc.

3. Use of Django signals. Django signals work as application triggers when an event associated with an object occurs.

4. Use of [aiohttp](https://docs.aiohttp.org/en/stable/) + asyncio to dispatch concurrent requests into the remote API.

## Proposal

I would use a combination of (2), (3) and (4)

## Additional notes

* If we have management rights on the remote API server I would have use **webhooks** to avoid the complexity of (2) + (3) + (4).

* If we just want to allow the scalibility at DDBB level and the DDBB has a high read/write ratio (way more READ queries than WRITE/UPDATE/DELETE ones), it might be useful to enable database replication, keeping a master-slave architecture. This architecture enable us to mantain a master database with one or more servers working on READ queries and ready to take
over if the primary server fails.
