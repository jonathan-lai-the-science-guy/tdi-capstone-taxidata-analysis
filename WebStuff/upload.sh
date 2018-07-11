#!/bin/bash
rsync -rav html /var/www
touch /var/www/html/*
touch /var/www/html/*/*
touch /var/www/html/*/*/*
