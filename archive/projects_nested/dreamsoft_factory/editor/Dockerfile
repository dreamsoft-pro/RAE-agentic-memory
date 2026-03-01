FROM nginx:stable

ENV NGX_WORKERS=1 \
    NGX_SRVNAME=_ \
    NGX_CONN=1024

COPY ./.docker_entrypoint /usr/bin/entrypoint.sh
COPY ./.docker_nginx.conf.tmp /etc/nginx/nginx.conf.tmp
WORKDIR /app
COPY . .

RUN apt-get update && apt-get -y install gettext nodejs npm
RUN npm install
RUN npm install -g gulp
RUN npm run compile
RUN gulp build --companyID='${companyID}' --domain='${domain}' --frameworkUrl='${frameworkUrl}' --backendUrl='${backendUrl}' --authUrl='${authUrl}' --staticUrl='${staticUrl}' --frontendUrl='${frontendUrl}'

RUN  chmod a+x /usr/bin/entrypoint.sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f ./.docker*

EXPOSE 80

ENTRYPOINT ["/usr/bin/entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]
