const express       = require('express');
const router        = express.Router();
module.exports      = router;

$$CONTROLLERS$$
$$MIDDLEWARE_IMPORT$$

// Home
router.get('/', (_req, res) => {
  res.status(200).send({ message: 'Welcome to Neutrino!' });
});

$$ROUTES$$

// Default response for any other request
router.use((_req, res) => {
  res.status(404).send({ message: "404 not found" });
});