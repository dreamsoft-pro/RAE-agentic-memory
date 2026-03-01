FROM golang:bullseye


RUN \
    apt-get update \
    && apt-get install -y mariadb-client bash \
    && go install github.com/rubenv/sql-migrate/...@latest \
    && mkdir -p /sql /sql-migrate

WORKDIR /app

COPY ./docker/sql-migrate/migrations /app
ADD ./docker/sql-migrate/docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

#CMD ["/bin/bash"]
