import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress, TextField } from '@mui/material';
import useApi from '../../hooks/useApi';
<$= "import authHeader from '../../services/auth-header';" if self.project.auth_object else "" $>
import '../../App.css';
import configData from '../../../config.json'

export default function <$= self.model.name $>Show(props) {
  const { id } = useParams();
  const navigate = useNavigate();
  const { result: $$name$$, loading, error, refresh } = useApi(`${configData.SERVER_URL}/$$name$$/${id}`);
  $$MANY_TO_MANY:0

  function handleDelete() {
    axios.delete(`${configData.SERVER_URL}/$$name$$/${id}`<%= "{ headers: authHeader() }" if self.project.auth_object else "" %>);
    navigate('/$$pluralname$$');
  }

  <$ begin if self.project.auth_object $>
  This is only included if auth object
  second line here
  <$ end $>

  <$ begin if not self.project.auth_object $>
  this is not auth objects
  should not happen
  <$ end $></$>

  <$ begin if False $>
  This should not show up
  <$ end $>

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
            onClick={() => navigate(`/$$name$$/${id}/edit`)}>edit
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
