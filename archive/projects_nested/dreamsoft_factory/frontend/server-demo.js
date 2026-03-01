var express = require('express');
var app = express();

app.use(express.static('app'));

app.use('/*', function(req, res){
  res.sendFile(__dirname + '/app/demo/index.html');
});



module.exports = app;
