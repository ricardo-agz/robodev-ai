import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { UserContext } from './UserContext';
import configData from "./config.json";

export default function useAuth() {
  const navigate = useNavigate();
  const { setAuthUser } = useContext(UserContext);
  const [error, setError] = useState(null);

  const setUserContext = () => {
    const auth = JSON.parse(localStorage.getItem('auth'));
    if (auth) {
      axios.get(`${configData.SERVER_URL}/user/${auth.id}`, 
        { headers: authHeader() })
        .then(r => {
          setAuthUser(r.data);
        })
        .catch(err => {
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
    setAuthUser(null);
    navigate('/');
  }

  // register
  const register = async (data) => {
		const { name, charity, username, email, password } = data;
    return axios.post(`${configData.SERVER_URL}/auth/register`, {
			name, charity, username, email, password
    })
    .then(res => {
      setUserContext();
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

