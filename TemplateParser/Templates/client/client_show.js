import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import useApi from '../../hooks/useApi';
$$AUTH:0
import '../../App.css';

export default function $$Name$$Show(props) {
  const { id } = useParams();
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
    return <div>loading...</div>;
  } else {
    return (
      <div className='container'>
        <h1>$$Name$$ {id}</h1>
        $$dynamic:0
        
        <div style={{display: "flex"}}>
          <Link to={`/$$name$$s/${id}/edit`}>
            <button className="submit">Edit</button>  
          </Link>
          <Link to={`/$$name$$s`}>
            <button className="submit" onClick={handleDelete}>Delete</button>  
          </Link>
        </div>

        $$ONE_TO_MANY:ONE
        $$MANY_TO_MANY:2
      </div>
    );
  }
}
