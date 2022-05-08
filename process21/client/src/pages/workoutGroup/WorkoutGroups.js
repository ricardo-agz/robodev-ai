import React from 'react';
import '../../App.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress } from '@mui/material';
import useApi from '../../hooks/useApi';
import authHeader from '../../services/auth-header';
import configData from '../../../config.json'

export default function WorkoutGroups() {
  const { result: workoutGroups, loading, error, refresh } = useApi(`${configData.SERVER_URL}/workoutgroups`);
  const navigate = useNavigate();

  function handleDelete(id) {
    axios.delete(`${configData.SERVER_URL}/workoutgroup/${id}`, { headers: authHeader() });
    window.location.reload();
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !workoutGroups) {
    return <CircularProgress />;
  } else {
    return (
      <div className='container'>
        <h1>Workout Groups</h1>
        <Button 
          variant={"contained"}
          onClick={() => navigate("/workoutgroups/new")}
        >
        New Workout Group
        </Button>

        <ul>
        {workoutGroups.map((workoutGroup, i) => (
          <div className="listItem" key={i}>
            <li key={i}>{workoutGroup.name}</li>
            <ButtonGroup variant="outlined" size="small">
              <Button onClick={() => navigate(`/workoutgroup/${workoutgroup._id}`)}>show</Button>
              <Button onClick={() => navigate(`/workoutgroup/${workoutgroup._id}/edit`)}>edit</Button>
              <Button color="error" onClick={() => handleDelete(workoutgroup._id)}>delete</Button>
            </ButtonGroup>
          </div>
        ))}
        </ul>
      </div>
    );
  };
};
