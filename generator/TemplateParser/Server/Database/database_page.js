const mongoose = require('mongoose');
require('dotenv').config();

const options = {
  useNewUrlParser: true,
  useUnifiedTopology: true,
};

const database = mongoose
  .connect(process.env.DB_CONNECTION, options)
  .then(() => console.log('Connected to database.'))
  .catch(err => console.error('Error connecting to database:', err.message));

module.exports = database;