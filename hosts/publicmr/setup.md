FROM php:5-apache

RUN apt-get install apache2

RUN apt-get install php

RUN apt-get update

RUN apt-get install -y php-pear

RUN pear channel-discover pear.nrk.io

RUN pear install nrk/Predis

