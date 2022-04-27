import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress, TextField } from '@mui/material';
import useApi from '../../hooks/useApi';
$$AUTH:0
import '../../App.css';

export default function $$Name$$Show(props) {
  const { id } = useParams();
  const navigate = useNavigate();
  const { result: $$name$$, loading, error, refresh } = useApi(`$$LINK$$/$$name$$s/${id}`);
  $$MANY_TO_MANY:0

  function handleDelete() {
    axios.delete(`$$LINK$$/$$name$$s/${id}`$$header$$);
    navigate('/$$name$$s');
  }

  $$MANY_TO_MANY:1

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !$$name$$) {
    return <CircularProgress />;
  } else {
    return (
      <div className='container'>
        <div className='row'>
          <h1 className='paddedRight'>$$Name$$ {id}</h1>

          <Button variant="outlined" style={{marginRight: 15}}
            onClick={() => navigate(`/$$name$$s/${id}/edit`)}>edit
          </Button>
          <Button variant="contained" color="error" 
            onClick={handleDelete}>delete
          </Button>
        </div>

        $$dynamic:0

        $$ONE_TO_MANY:ONE
        $$MANY_TO_MANY:2
      </div>
    );
  }
}
