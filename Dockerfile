# Dockerfile
FROM python:3.11
WORKDIR app/
ENV PIP_ROOT_USER_ACTION=ignore

# Pip packages installation
RUN pip install --upgrade pip
COPY requirements/production.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy only required files and folders
COPY manage.py /app
COPY start.sh /app
COPY .env-files/production /app/.env
COPY api /app/api
COPY rindusrest /app/rindusrest
