$$AUTH$$:0

const AuthController = {
  login: async (req, res) => {
    const $$name$$ = await $$Name$$.findOne({ username: req.body.username });
    if (!$$name$$) return res.status(400).json({ message: "Invalid username" });

    const checkpassword = await bcrypt.compare(req.body.password, $$name$$.password);
    if (!checkpassword) return res.status(400).json({ message: "Incorrect password" });

    const payload = {
      id: $$name$$._id.toString(),
      username: $$name$$.username,
    }
    jwt.sign(
      payload,
      process.env.JWT_SECRET, { expiresIn: 86400 },
      (err, token) => {
        if (err) return res.json({ message: err });
        return res.json({
          id: $$name$$._id.toString(),
          token: "Bearer " + token
        });
      }
    );
  },

  register: async (req, res) => {
    const $$name$$ = req.body;      
    const takenUsername = await $$Name$$.findOne({ username: $$name$$.username });
    const takenEmail = await $$Name$$.findOne({ email: $$name$$.email });

    if (takenUsername) {
      res.status(400).json({ message: "Username already taken" });
    } else if (takenEmail) {
      res.status(400).json({ message: "Email already exists" });
    } else {
      $$name$$.password = await bcrypt.hash(req.body.password, 10);
      $$name$$.email = $$name$$.email.toLowerCase();
      $$name$$.username = $$name$$.username.toLowerCase();
      const db$$Name$$ = new $$Name$$($$name$$);
      db$$Name$$.save();
      res.json({ message: "Success" });
    }
  }
}

module.exports = AuthController;