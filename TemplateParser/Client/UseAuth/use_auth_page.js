import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { $$Name$$Context } from './$$Name$$Context';
import configData from '../config.json';
import authHeader from '../services/auth-header';

export default function useAuth() {
  const navigate = useNavigate();
  const { setAuth$$Name$$ } = useContext($$Name$$Context);
  const [error, setError] = useState(null);

  const set$$Name$$Context = () => {
    const auth = JSON.parse(localStorage.getItem('auth'));
    if (auth) {
      axios.get(`${configData.SERVER_URL}/<$= self.model.plural.lower() $>/${auth.id}`, 
        { headers: authHeader() })
        .then(r => {
          setAuth$$Name$$(r.data);
        })
        .catch(err => {
          setAuth$$Name$$(null);
          setError(err.response.data);
        });
      navigate('../');
    };
  };

  // login
  const login = (username, password) => {
    setError(null);
    axios.post(`${configData.SERVER_URL}/auth/login`, {
      username: username,
      password: password
    })
    .then((res) => {
      if (res.data.token) {
        localStorage.setItem("auth", JSON.stringify(res.data));
        setUserContext();
      }
      return res.data;
    })
    .catch((err) => {
      setError(err.response.data.message);
    });
  }

  // logout
  const logout = () => {
    localStorage.removeItem('auth');
    setAuth$$Name$$(null);
    navigate('/');
  }

  // register
  const register = async (data) => {
    $$DECLARE_REGISTER_DATA$$
    return axios.post(`${configData.SERVER_URL}/auth/register`, {
      $$REGISTER_DATA$$
    })
    .then(res => {
      set$$Name$$Context();
    })
    .catch(err => {
      setError(err.response.data.message);
    });
  };

  return {
    login,
    logout,
    register,
    error
  }
}

