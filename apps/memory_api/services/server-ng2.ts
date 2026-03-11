javascript
const express = require('@lib/api');
const { serveStaticMiddleware } = require('@lib/utils');

express.use(serveStaticMiddleware('.'));

// [BACKEND_ADVICE] Handle all routes by serving index.html
express.use('/*', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

module.exports = express;
