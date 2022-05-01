import React, { useContext } from 'react'
import { useNavigate } from 'react-router-dom';
import { $$Name$$Context } from '../hooks/$$Name$$Context';
import useAuth from '../hooks/useAuth';

export default function Nav() {
  const { auth$$Name$$ } = useContext($$Name$$Context);
  const { logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="nav">
      {auth$$Name$$ ?
        <div className='row'>
          <div 
            onClick={() => navigate(`/users/${auth$$Name$$._id}`)}
            className='clickable'>hi {auth$$Name$$.username}</div>
          <div 
            onClick={logout}
            className='clickable'>logout</div>
        </div>
        :
        <div className='row'>
          <div className='clickable' onClick={() => navigate('login')}>login</div>
          <div className='clickable' onClick={() => navigate('register')}>register</div>
        </div>
      }
    </div>
  )
}