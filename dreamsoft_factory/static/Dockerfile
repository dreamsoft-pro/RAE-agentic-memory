FROM nginx:stable-alpine

ENV STATIC_PATH=/var/www/app

COPY ./app.conf /etc/nginx/app.conf.tmp
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod a+x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
