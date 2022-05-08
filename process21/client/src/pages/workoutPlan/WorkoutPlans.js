import React from 'react';
import '../../App.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress } from '@mui/material';
import useApi from '../../hooks/useApi';
import authHeader from '../../services/auth-header';
import configData from '../../../config.json'

export default function WorkoutPlans() {
  const { result: workoutPlans, loading, error, refresh } = useApi(`${configData.SERVER_URL}/workoutplans`);
  const navigate = useNavigate();

  function handleDelete(id) {
    axios.delete(`${configData.SERVER_URL}/workoutplan/${id}`, { headers: authHeader() });
    window.location.reload();
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !workoutPlans) {
    return <CircularProgress />;
  } else {
    return (
      <div className='container'>
        <h1>Workout Plans</h1>
        <Button 
          variant={"contained"}
          onClick={() => navigate("/workoutplans/new")}
        >
        New Workout Plan
        </Button>

        <ul>
        {workoutPlans.map((workoutPlan, i) => (
          <div className="listItem" key={i}>
            <li key={i}>{workoutPlan.target_days}</li>
            <ButtonGroup variant="outlined" size="small">
              <Button onClick={() => navigate(`/workoutplan/${workoutplan._id}`)}>show</Button>
              <Button onClick={() => navigate(`/workoutplan/${workoutplan._id}/edit`)}>edit</Button>
              <Button color="error" onClick={() => handleDelete(workoutplan._id)}>delete</Button>
            </ButtonGroup>
          </div>
        ))}
        </ul>
      </div>
    );
  };
};
