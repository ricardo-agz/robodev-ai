import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress, TextField } from '@mui/material';
import useApi from '../../hooks/useApi';
import authHeader from '../../services/auth-header';
import '../../App.css';
import configData from '../../../config.json'

export default function WorkoutGroupShow(props) {
  const { id } = useParams();
  const navigate = useNavigate();
  const { result: workoutgroup, loading, error, refresh } = useApi(`${configData.SERVER_URL}/workoutgroup/${id}`);
	const [memberId, setMemberId] = useState();

  function handleDelete() {
    axios.delete(`${configData.SERVER_URL}/workoutgroup/${id}`<%= "{ headers: authHeader() }" if self.project.auth_object else "" %>);
    navigate('/workoutgroups');
  }

  This is only included if auth object
  second line here




  function addMember() {
    try {
    } catch (e) {
      console.log(e);
    };
    window.location.reload();
  };

  function dropMember(droppedId) {
    try {
      axios.post(`${configData.SERVER_URL}/workoutgroup/${id}/drop-member/${droppedId}`,
				{}, { headers: authHeader() });
    } catch (e) {
      console.log(e);
    };
    window.location.reload();
  };

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !workoutgroup) {
    return <CircularProgress />;
  } else {
    return (
      <div className='container'>
        <div className='row'>
          <h1 className='paddedRight'>WorkoutGroup {id}</h1>

          <Button variant="outlined" style={{marginRight: 15}}
            onClick={() => navigate(`/workoutgroup/${id}/edit`)}>edit
          </Button>
          <Button variant="contained" color="error" 
            onClick={handleDelete}>delete
          </Button>
        </div>


      </div>
    );
  }
}
