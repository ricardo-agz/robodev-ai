import { useState, useEffect } from 'react';
import authHeader from '../services/auth-header';
import configData from "./config.json";

export default function useFind$$Name$$() {
  const [$$nameCamel$$, set$$Name$$] = useState(null);

  useEffect(() => {
    const auth = JSON.parse(localStorage.getItem('auth'));
    if (auth) {
      axios.get(`${configData.SERVER_URL}/$$name$$/${auth.id}`, 
        { headers: authHeader() })
        .then(r => {
          set$$Name$$(r.data);
        })
        .catch(err => {
          console.log(err);
        });
    };
  }, []);

  return {
    $$nameCamel$$,
    set$$Name$$
  }
}
