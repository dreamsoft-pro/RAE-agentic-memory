FROM node:18-bookworm

WORKDIR /app

RUN apt-get update && apt-get -y install git nginx gettext \
  && apt-get -y clean && rm -rf /var/lib/apt/lists/*

COPY ./.docker_entrypoint /usr/bin/entrypoint.sh
COPY ./.docker_nginx.conf /etc/nginx/nginx.conf.tmp
RUN chmod a+x /usr/bin/entrypoint.sh

ENV NGX_WORKERS=1 \
    NGX_SRVNAME=_ \
    NGX_CONN=1024

COPY ./ /app
RUN rm ./.docker*
RUN npm install -g grunt grunt-cli
RUN npm install grunt-parallel

RUN npm install

EXPOSE 80

ENTRYPOINT ["/usr/bin/entrypoint.sh"]

CMD ["/usr/sbin/nginx"]
