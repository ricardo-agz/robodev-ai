import React from 'react';
import '../../App.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress } from '@mui/material';
import useApi from '../../hooks/useApi';
import authHeader from '../../services/auth-header';
import configData from '../../../config.json'

export default function MonthlyPledges() {
  const { result: monthlyPledges, loading, error, refresh } = useApi(`${configData.SERVER_URL}/monthlypledges`);
  const navigate = useNavigate();

  function handleDelete(id) {
    axios.delete(`${configData.SERVER_URL}/monthlypledge/${id}`, { headers: authHeader() });
    window.location.reload();
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !monthlyPledges) {
    return <CircularProgress />;
  } else {
    return (
      <div className='container'>
        <h1>Monthly Pledges</h1>
        <Button 
          variant={"contained"}
          onClick={() => navigate("/monthlypledges/new")}
        >
        New Monthly Pledge
        </Button>

        <ul>
        {monthlyPledges.map((monthlyPledge, i) => (
          <div className="listItem" key={i}>
            <li key={i}>{monthlyPledge.payment_amount}</li>
            <ButtonGroup variant="outlined" size="small">
              <Button onClick={() => navigate(`/monthlypledge/${monthlypledge._id}`)}>show</Button>
              <Button onClick={() => navigate(`/monthlypledge/${monthlypledge._id}/edit`)}>edit</Button>
              <Button color="error" onClick={() => handleDelete(monthlypledge._id)}>delete</Button>
            </ButtonGroup>
          </div>
        ))}
        </ul>
      </div>
    );
  };
};
