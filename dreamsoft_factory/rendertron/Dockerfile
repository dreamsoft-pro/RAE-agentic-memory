FROM ubuntu


RUN cat /etc/apt/sources.list && apt update

RUN echo /etc/apt/sources.list
RUN    apt update \
    && apt install -y wget gnupg git curl

COPY --from=node:10-slim /usr/local/bin /usr/local/bin
COPY --from=node:10-slim /usr/local/lib/node_modules /usr/local/lib/node_modules

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst  libxshmfence1 libglu1 fonts-freefont-ttf libxss1 \
    --no-install-recommends \
    && apt install libxshmfence1 libglu1 \
    && rm -rf /var/lib/apt/lists/*


# This directoty will store cached files as specified in the config.json.
# If you haven't defined the cacheConfig.snapshotDir property you can remove the following line
RUN mkdir /cache

RUN git clone https://github.com/GoogleChrome/rendertron.git

WORKDIR /rendertron

RUN npm install && npm run build

# If you aren't using a custom config.json file you must remove the following line
#ADD config.json .

EXPOSE 3000

CMD ["node", "build/rendertron.js"]
