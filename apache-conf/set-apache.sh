#!/bin/bash
#cp default-ssl.conf /etc/apache2/sites-enabled/default-ssl.conf
cp httpd.conf /etc/apache2/httpd.conf

a2enmod cgid
a2enmod expires
a2enmod rewrite
