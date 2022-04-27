import React, { useContext } from 'react'
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../hooks/UserContext';
import useAuth from '../hooks/useAuth';

export default function Nav() {
  const { authUser } = useContext(UserContext);
  const { logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="nav">
      {authUser ?
        <div className='row'>
          <div 
            onClick={() => navigate(`/users/${authUser._id}`)}
            className='clickable'>hi {authUser.username}</div>
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