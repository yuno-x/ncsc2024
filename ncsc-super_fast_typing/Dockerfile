FROM php:8.2-apache

RUN chmod 1733 /tmp /var/tmp; \
    sed -i "s/\(Options Indexes.*\)/# \1/" /etc/apache2/apache2.conf; \
    echo "ServerTokens ProductOnly" >> /etc/apache2/apache2.conf; \
    echo "ServerSignature off" >> /etc/apache2/apache2.conf;

