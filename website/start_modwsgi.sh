#!/bin/sh

#Configuration on how to start the server
python manage.py runmodwsgi \
--server-root /etc/wsgi-port-80 \
--user www-data --group www-data \
--port 80 --setup-only \
--https-only \
--https-port 443 \
--ssl-certificate-file "/etc/letsencrypt/live/www.dimsum.dk/cert.pem" \
--ssl-certificate-key-file "/etc/letsencrypt/live/www.dimsum.dk/privkey.pem" \
--server-name 'www.dimsum.dk'

#Starting the server
sudo /etc/wsgi-port-80/apachectl stop
sudo /etc/wsgi-port-80/apachectl start
