#!/bin/bash

# create job scheduler, run tasks that have been scheduled and start the server 
python manage.py expire_events & python manage.py process_tasks & gunicorn --access-logfile - --error-logfile - -b 0.0.0.0:8080 -t 300 --threads 16 send.wsgi:application 