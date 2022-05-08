import React from 'react';
import '../../App.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress } from '@mui/material';
import useApi from '../../hooks/useApi';
import authHeader from '../../services/auth-header';
import configData from '../../../config.json'

export default function PaymentMethods() {
  const { result: paymentMethods, loading, error, refresh } = useApi(`${configData.SERVER_URL}/paymentmethods`);
  const navigate = useNavigate();

  function handleDelete(id) {
    axios.delete(`${configData.SERVER_URL}/paymentmethod/${id}`, { headers: authHeader() });
    window.location.reload();
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !paymentMethods) {
    return <CircularProgress />;
  } else {
    return (
      <div className='container'>
        <h1>Payment Methods</h1>
        <Button 
          variant={"contained"}
          onClick={() => navigate("/paymentmethods/new")}
        >
        New Payment Method
        </Button>

        <ul>
        {paymentMethods.map((paymentMethod, i) => (
          <div className="listItem" key={i}>
            <li key={i}>{paymentMethod.card_number}</li>
            <ButtonGroup variant="outlined" size="small">
              <Button onClick={() => navigate(`/paymentmethod/${paymentmethod._id}`)}>show</Button>
              <Button onClick={() => navigate(`/paymentmethod/${paymentmethod._id}/edit`)}>edit</Button>
              <Button color="error" onClick={() => handleDelete(paymentmethod._id)}>delete</Button>
            </ButtonGroup>
          </div>
        ))}
        </ul>
      </div>
    );
  };
};
