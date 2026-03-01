FROM node:16-alpine

WORKDIR /app

COPY ./.docker_entrypoint /usr/bin/entrypoint.sh
RUN chmod a+x /usr/bin/entrypoint.sh

COPY ./ /app
RUN rm ./.docker*
RUN npm install

EXPOSE 80

ENTRYPOINT ["/usr/bin/entrypoint.sh"]

CMD ["node", "app.js"]
