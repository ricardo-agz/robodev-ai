import { useState, useEffect } from 'react';
import authHeader from '../services/auth-header';
import configData from "./config.json";

export default function useFindUser() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const auth = JSON.parse(localStorage.getItem('auth'));
    if (auth) {
      axios.get(`${configData.SERVER_URL}/user/${auth.id}`, 
        { headers: authHeader() })
        .then(r => {
          setUser(r.data);
        })
        .catch(err => {
          console.log(err);
        });
    };
  }, []);

  return {
    user,
    setUser
  }
}
