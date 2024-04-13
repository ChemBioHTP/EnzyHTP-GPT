var express = require('express');
var path = require('path');
var app = express();
var favicon = require('serve-favicon')

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'build')));
app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')))

// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port: ${port}`);
});
