import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress, TextField } from '@mui/material';
import useApi from '../../hooks/useApi';
import authHeader from '../../services/auth-header';
import '../../App.css';
import configData from '../../../config.json'

export default function WorkoutPlanShow(props) {
  const { id } = useParams();
  const navigate = useNavigate();
  const { result: workoutplan, loading, error, refresh } = useApi(`${configData.SERVER_URL}/workoutplan/${id}`);

  function handleDelete() {
    axios.delete(`${configData.SERVER_URL}/workoutplan/${id}`<%= "{ headers: authHeader() }" if self.project.auth_object else "" %>);
    navigate('/workoutplans');
  }

  This is only included if auth object
  second line here




  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !workoutplan) {
    return <CircularProgress />;
  } else {
    return (
      <div className='container'>
        <div className='row'>
          <h1 className='paddedRight'>WorkoutPlan {id}</h1>

          <Button variant="outlined" style={{marginRight: 15}}
            onClick={() => navigate(`/workoutplan/${id}/edit`)}>edit
          </Button>
          <Button variant="contained" color="error" 
            onClick={handleDelete}>delete
          </Button>
        </div>


      </div>
    );
  }
}
