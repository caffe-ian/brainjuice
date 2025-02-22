const express = require('express');

const app = express(); // Our App
const port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log('Connected to server');
})

app.use(express.static(__dirname/*, {
 maxAge: 86400000 * 30
}*/));

process.on('uncaughtException', (err) => {
  console.log("Fatal Error:", err);
});

app.use('/api/image', express.static('image'));
app.use('/api/metadata', express.static('metadata'));

app.use(function (request, response, next) {
  response.sendStatus(404);
});
