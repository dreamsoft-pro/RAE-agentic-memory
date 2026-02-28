/*
Copyright 2018 Google LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
// server.js
// where your node app starts
// load dependencies
const express = require('express');
const app = express();
const rendertron = require('rendertron-middleware');
const PORT = process.env.PORT || 3000;
const DIST_FOLDER = process.cwd() + '/public';

// Add googlebot to the list of bots we will use Rendertron for
const BOTS = rendertron.botUserAgents.concat('googlebot');
const BOT_UA_PATTERN = new RegExp(BOTS.join('|'), 'i');

app.set('view engine', 'html');

// Add Rendertron middleware to send bot requests to Rendertron
app.use(rendertron.makeMiddleware({
  proxyUrl: 'https://render-tron.appspot.com/render', // this is a DEMO URL! Do not use this in production!
  userAgentPattern: BOT_UA_PATTERN
}));

// Static Assets
app.get('*.*', express.static('public'));

// Point all routes to index...
app.get('*', (req, res) => {
  res.set('Vary', 'User-Agent');
  res.sendFile(DIST_FOLDER + '/index.html');
});

// Start Express Server
app.listen(PORT, () => {
  console.log(`Node Express server listening on ${PORT}`);
});