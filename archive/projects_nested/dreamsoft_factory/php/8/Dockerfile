FROM ubuntu:jammy as final

ENV PHP_MAX_CHILDREN=5 \
    PHP_START_SERVERS=2 \
    PHP_MIN_SPARE=1 \
    PHP_MAX_SPARE=3 \
    PHP_ERROR_REPORTING="E_ALL" \
    NGINX_GZIP=on \
    NGINX_REAL_IP="10.0.0.0/8"

WORKDIR /var/www/

COPY .docker_supervisor /etc/supervisor/conf.d/supervisor.conf
COPY .docker_nginx /etc/nginx/app.conf.tmp
COPY .docker_fpm /etc/php/8.1/fpm/pool.d/www.conf.tmp
COPY .docker_fpmconf /etc/php/8.1/fpm/php-fpm.conf
COPY .docker_preconfig /usr/bin/preconfig.sh

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt-get install -y -o Dpkg::Options::="--force-confold" \
    php-fpm libxml2 gettext-base supervisor php-mbstring php-xml php-bcmath php-soap php-mysql php-mongodb php-imagick php-curl php-gd php-zip unzip nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /var/log/nginx/*.log \
    && rm /etc/nginx/sites-enabled/default \
    && ln -s /dev/stdout /var/log/nginx/access.log \
    && ln -s /dev/stderr /var/log/nginx/error.log \
    && chmod a+x /usr/bin/preconfig.sh

EXPOSE 80 443

ENTRYPOINT ["/usr/bin/preconfig.sh"]

CMD ["/usr/bin/supervisord"]
