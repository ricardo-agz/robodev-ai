import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress, TextField } from '@mui/material';
import useApi from '../../hooks/useApi';
import authHeader from '../../services/auth-header';
import '../../App.css';
import configData from '../../../config.json'

export default function UserShow(props) {
  const { id } = useParams();
  const navigate = useNavigate();
  const { result: user, loading, error, refresh } = useApi(`${configData.SERVER_URL}/user/${id}`);
	const [workoutGroupId, setWorkoutGroupId] = useState();
	const [friendId, setFriendId] = useState();

  function handleDelete() {
    axios.delete(`${configData.SERVER_URL}/user/${id}`<%= "{ headers: authHeader() }" if self.project.auth_object else "" %>);
    navigate('/users');
  }

  This is only included if auth object
  second line here




  function addWorkoutGroup() {
    try {
    } catch (e) {
      console.log(e);
    };
    window.location.reload();
  };

  function dropWorkoutGroup(droppedId) {
    try {
      axios.post(`${configData.SERVER_URL}/user/${id}/drop-workoutgroup/${droppedId}`,
				{}, { headers: authHeader() });
    } catch (e) {
      console.log(e);
    };
    window.location.reload();
  };

  function addFriend() {
    try {
    } catch (e) {
      console.log(e);
    };
    window.location.reload();
  };

  function dropFriend(droppedId) {
    try {
      axios.post(`${configData.SERVER_URL}/user/${id}/drop-friend/${droppedId}`,
				{}, { headers: authHeader() });
    } catch (e) {
      console.log(e);
    };
    window.location.reload();
  };

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !user) {
    return <CircularProgress />;
  } else {
    return (
      <div className='container'>
        <div className='row'>
          <h1 className='paddedRight'>User {id}</h1>

          <Button variant="outlined" style={{marginRight: 15}}
            onClick={() => navigate(`/user/${id}/edit`)}>edit
          </Button>
          <Button variant="contained" color="error" 
            onClick={handleDelete}>delete
          </Button>
        </div>



        {/* User PaymentMethods */}
        <h3>PaymentMethods</h3>
          <Link to={`/users/${id}/paymentmethods/new`}>
            <button>New PaymentMethod</button>  
          </Link>
          <ul>

          {user.paymentMethods && user.paymentMethods.map((paymentMethod, i) => (
            <div className="listItem" key={i}>
              <li>{paymentMethod.card_number}</li>
              <Link to={`/paymentmethods/${paymentMethod._id}`}>
                <button className="listButton">show</button>
              </Link>
            </div>
          ))}
        </ul>

        {/* User MonthlyPledges */}
        <h3>MonthlyPledges</h3>
          <Link to={`/users/${id}/monthlypledges/new`}>
            <button>New MonthlyPledge</button>  
          </Link>
          <ul>

          {user.monthlyPledges && user.monthlyPledges.map((monthlyPledge, i) => (
            <div className="listItem" key={i}>
              <li>{monthlyPledge.payment_amount}</li>
              <Link to={`/monthlypledges/${monthlyPledge._id}`}>
                <button className="listButton">show</button>
              </Link>
            </div>
          ))}
        </ul>
      </div>
    );
  }
}
