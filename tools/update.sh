#!/usr/bin/env bash

git pull origin master
workon kabeta
pip install -r requirements.txt
sudo systemctl restart uwsgi
sudo systemctl restart celery
