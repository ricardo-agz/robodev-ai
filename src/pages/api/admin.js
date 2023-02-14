import bcrypt from 'bcrypt';

const PASSWORD_HASH = '$2b$10$6w5OEQw2lrnq0.MZkNar6ej9ipo1qVwJfiO1oV6Ndvh/vcAOfBjR2';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).end(); // Method Not Allowed
    return;
  }

  const { password } = req.body;
  const passwordMatches = await bcrypt.compare(password, PASSWORD_HASH);

  if (passwordMatches) {
    res.status(200).json({ message: 'Welcome to the admin panel!' });
  } else {
    res.status(401).json({ message: 'Incorrect password.' });
  }
}
