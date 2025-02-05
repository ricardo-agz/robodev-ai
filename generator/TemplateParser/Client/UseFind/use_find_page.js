import { useState, useEffect } from 'react';
import axios from 'axios';
import authHeader from '../services/auth-header';
import configData from '../config.json';

export default function useFind$$Name$$() {
  const [$$nameCamel$$, set$$Name$$] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const auth = JSON.parse(localStorage.getItem('auth'));
    if (auth) {
      axios.get(`${configData.SERVER_URL}/<$= self.model.plural.lower() $>/${auth.id}`, 
        { headers: authHeader() })
        .then(r => {
          set$$Name$$(r.data);
        })
        .catch(err => {
          set$$Name$$(null);
          localStorage.removeItem('auth');
          console.log(err);
        })
        .then(() => {
          setLoading(false);
        })
    };
  }, []);

  return {
    $$nameCamel$$,
    set$$Name$$,
    loading
  }
}
