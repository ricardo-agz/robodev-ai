<<<<<<< HEAD
const express       = require('express');
const router        = express.Router();
module.exports      = router;
=======
const express = require('express');
const router = express.Router();
module.exports = router;
>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3

$$CONTROLLERS$$
$$AUTH_CONTROLLER$$
$$MIDDLEWARE_IMPORT$$

<<<<<<< HEAD

=======
>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3
// Home
router.get('/', (_req, res) => {
  res.status(200).send({ message: 'Welcome to Neutrino!' });
});

$$ROUTES$$
$$AUTH_ROUTES$$
// Default response for any other request
router.use((_req, res) => {
  res.status(404).send({ message: "404 not found" });
});