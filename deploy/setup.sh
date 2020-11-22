#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.ss
PROJECT_GIT_URL='https://github.com/DSM-PEAR/admin_backend.git'

PROJECT_BASE_PATH='/usr/local/apps/Pear_Admin'

echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

# Create project directory
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Create virtual environment
mkdir -p $PROJECT_BASE_PATH/env
python3 -m venv $PROJECT_BASE_PATH/env

# Install python packages
$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
$PROJECT_BASE_PATH/env/bin/pip install uwsgi==2.0.18

# Run migrations and collectstatic
cd $PROJECT_BASE_PATH
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput

# Configure supervisor
cp $PROJECT_BASE_PATH/deploy/supervisor_Pear_Admin_app.conf /etc/supervisor/conf.d/Pear_Admin_app.conf
supervisorctl reread
supervisorctl update
supervisorctl restart Pear_Admin_app

# Configure nginx
cp $PROJECT_BASE_PATH/deploy/nginx_Pear_Admin_app.conf /etc/nginx/sites-available/Pear_Admin_app.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/nginx_Pear_Admin_app.conf /etc/nginx/sites-enabled/Pear_Admin_app.conf
systemctl restart nginx.service

echo "DONE! :)"
