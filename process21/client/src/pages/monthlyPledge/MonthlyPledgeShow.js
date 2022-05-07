import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress, TextField } from '@mui/material';
import useApi from '../../hooks/useApi';
import authHeader from '../../services/auth-header';
import '../../App.css';
import configData from '../../../config.json'

export default function MonthlyPledgeShow(props) {
  const { id } = useParams();
  const navigate = useNavigate();
  const { result: monthlypledge, loading, error, refresh } = useApi(`${configData.SERVER_URL}/monthlypledge/${id}`);

  function handleDelete() {
    axios.delete(`${configData.SERVER_URL}/monthlypledge/${id}`<%= "{ headers: authHeader() }" if self.project.auth_object else "" %>);
    navigate('/monthlypledges');
  }

  This is only included if auth object
  second line here




  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !monthlypledge) {
    return <CircularProgress />;
  } else {
    return (
      <div className='container'>
        <div className='row'>
          <h1 className='paddedRight'>MonthlyPledge {id}</h1>

          <Button variant="outlined" style={{marginRight: 15}}
            onClick={() => navigate(`/monthlypledge/${id}/edit`)}>edit
          </Button>
          <Button variant="contained" color="error" 
            onClick={handleDelete}>delete
          </Button>
        </div>



        {/* MonthlyPledge Workoutplans */}
        <h3>Workoutplans</h3>
          <Link to={`/monthlypledges/${id}/workoutplans/new`}>
            <button>New Workoutplan</button>  
          </Link>
          <ul>

          {monthlyPledge.workoutplans && monthlyPledge.workoutplans.map((workoutplan, i) => (
            <div className="listItem" key={i}>
              <li>{workoutplan.target_days}</li>
              <Link to={`/workoutplans/${workoutplan._id}`}>
                <button className="listButton">show</button>
              </Link>
            </div>
          ))}
        </ul>
      </div>
    );
  }
}
