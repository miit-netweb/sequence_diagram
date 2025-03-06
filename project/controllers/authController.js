const bcrypt = require('bcrypt');
const User = require('../models/User');
const { generateToken } = require('../config/jwt');

const register = async (req, res) => {
  try {
    const hashedPassword = await bcrypt.hash(req.body.password, 10);
    const user = new User({
      username: req.body.username,
      password: hashedPassword,
    });
    await user.save();
    res.status(201).send('User created');
  } catch (err) {
    res.status(500).send(err.message);
  }
};

const login = async (req, res) => {
  const user = await User.findOne({ username: req.body.username });
  if (!user) return res.status(400).send('Cannot find user');

  try {
    if (await bcrypt.compare(req.body.password, user.password)) {
      const accessToken = generateToken({ userId: user._id, username: user.username });
      res.json({ accessToken });
    } else {
      res.send('Not Allowed');
    }
  } catch (err) {
    res.status(500).send(err.message);
  }
};

module.exports = { register, login };