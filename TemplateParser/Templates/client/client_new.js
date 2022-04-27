import React, { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import axios from 'axios';
$$AUTH:0
import '../../App.css';

export default function $$Name$$New() {
  $$ONE_TO_MANY:MANY
	$$dynamic:0

	const handleSubmit = () => {
		axios.post('$$LINK$$/$$name$$s', 
    {
      $$dynamic:1
    }$$header$$)
    .then(res => {
      navigate("/$$name$$s")
    })
    .catch(err => {
      alert(err)
    })
	};

	return (
		<div className='container'>
			<h1>New $$Name$$</h1>
			$$dynamic:2
			<Link to='/$$name$$s'>
				<button onClick={handleSubmit} className='submit'>Submit</button>
			</Link>
		</div>
	)
}
