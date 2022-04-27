import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ValidatedForm from './ValidatedForm';
import axios from 'axios';
import useApi from '../../hooks/useApi';
$$AUTH:0
import { CircularProgress } from '@mui/material';
import '../../App.css';

export default function $$Name$$Edit() {
	const { id } = useParams();
  const { result: $$name$$, loading, error, refresh } = useApi(`$$LINK$$/$$name$$s/${id}`);
  const navigate = useNavigate();

	$$dynamic:1
    axios.put(`$$LINK$$/$$name$$s/${id}/edit`, 
    {
      $$dynamic:0
    }$$header$$)
    .then(res => {
      navigate(`/$$name$$s/${id}`)
    })
    .catch(err => {
      alert(err.response.data.message);
    });
	};

	if (error) {
		return <div>Error: {error.message}</div>;
	} else if (loading || !$$name$$) {
		return <CircularProgress />;
	} else {
		return (
			<div className='container'>
				<h1>Edit $$Name$$</h1>
				$$dynamic:2
			</div>
		)
	}
}
