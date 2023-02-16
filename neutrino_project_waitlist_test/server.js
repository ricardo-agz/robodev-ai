const express     = require('express');
const cors        = require('cors');

require('./config/database');

const app         = express();
const routes      = require('./routes/routes');
const PORT        = process.env.PORT || 8080;
const corsOptions = {
  origin: "*"
}

app.use( express.json() );
app.use( cors(corsOptions) );
app.use('/', routes);

app.listen(
	PORT,
	console.log(`Server running on http://localhost:${PORT}...`)
);