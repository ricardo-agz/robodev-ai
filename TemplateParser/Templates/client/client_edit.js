import React, { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
$$AUTH:0
import '../../App.css';

export default function $$Name$$Edit() {
	const { id } = useParams();	
  const [$$name$$, set$$Name$$] = useState(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(false);
  $$dynamic:0

	useEffect(() => {
		axios.get(`$$LINK$$/$$name$$s/${id}`$$header$$)
		.then((res) => {
			set$$Name$$(res.data);
			setLoading(false);
      navigate("/$$name$$s")
		})
		.catch((err) => {
			console.log(err);
			setError(err);
		});
	}, []);

	useEffect(() => {
		if ($$name$$) {
			$$dynamic:1
		}
	}, [$$name$$]);

	const handleSubmit = () => {
		try {
			axios.put(`$$LINK$$/$$name$$s/${id}/edit`, 
      {
				$$dynamic:2
			}$$header$$)
		} catch (e) {
			console.log(e);
		};
	};

	if (error) {
		return <div>Error: {error.message}</div>;
	} else if (loading) {
		return <div>Loading...</div>;
	} else {
		return (
			<div className='container'>
				<h1>Edit $$Name$$</h1>
				$$dynamic:3
				<button onClick={handleSubmit} className='submit'>Submit</button>
			</div>
		)
	}
}
