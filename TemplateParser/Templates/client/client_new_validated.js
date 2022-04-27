import React from 'react';
import { useNavigate } from 'react-router-dom';
import ValidatedForm from './ValidatedForm';
import axios from 'axios';
$$AUTH:0
import '../../App.css';

export default function $$Name$$New() {
  const navigate = useNavigate();

	$$dynamic:0
		axios.post('$$LINK$$/$$name$$s', {
      $$dynamic:1
    }$$header$$)
    .then(res => {
      navigate("/$$name$$s")
    })
    .catch(err => {
      alert(err.response.data.message);
    })
	};

	return (
		<div className='container'>
			<h1>New $$Name$$</h1>
			$$dynamic:2
		</div>
	)
}
