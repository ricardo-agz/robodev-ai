import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress } from '@mui/material';
import useApi from '../../hooks/useApi';
$$AUTH:0
import '../../App.css';

export default function $$Name$$s() {
  const { result: $$name$$s, loading, error, refresh } = useApi("$$LINK$$/$$name$$s");
  const navigate = useNavigate();

  function handleDelete(id) {
    axios.delete(`$$LINK$$/$$name$$s/${id}`$$header$$)
    window.location.reload();
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !$$name$$s) {
    return <CircularProgress />;
  } else {
    return (
      <div className='container'>
        <h1>$$Name$$s</h1>
        <Button variant={"contained"} onClick={() => navigate("/$$name$$s/new")}>new $$name$$</Button>

        <ul>
        {$$name$$s.map(($$name$$, i) => (
          <div className="listItem" key={i}>
            $$dynamic:0
            <ButtonGroup variant="outlined" size="small">
              <Button onClick={() => navigate(`/$$name$$s/${$$name$$._id}`)}>show</Button>
              <Button onClick={() => navigate(`/$$name$$s/${$$name$$._id}/edit`)}>edit</Button>
              <Button color="error" onClick={() => handleDelete($$name$$._id)}>delete</Button>
            </ButtonGroup>
          </div>
        ))}
        </ul>
      </div>
    )
  }
}
