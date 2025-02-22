import { OpenSeaStreamClient } from '@opensea/stream-js';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const express = require('express');

const app = express(); // Our App
const port = process.env.PORT || 3000;

// const client = new OpenSeaStreamClient({
//     token: 'openseaApiKey'
// });

app.listen(port, () => {
  console.log('Connected to server');
})

process.on('uncaughtException', (err) => {
  console.log("Fatal Error:", err);
});

app.use(function (request, response, next) {
  response.sendStatus(404);
});
