import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import useApi from '../../hooks/useApi';
$$AUTH:0
import '../../App.css';

export default function $$Name$$s() {
  const { result: $$name$$s, loading, error, refresh } = useApi("$$LINK$$/$$name$$s");

  function handleDelete(id) {
    axios.delete(`$$LINK$$/$$name$$s/${id}`$$header$$)
    window.location.reload();
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !$$name$$s) {
    return <div>loading...</div>;
  } else {
    return (
      <div className='container'>
        <h1>$$Name$$s</h1>

        <Link to="/$$name$$s/new">
          <button className="submit">New $$Name$$</button> 
        </Link>

        <ul>
        {$$name$$s.map(($$name$$, i) => (
          <div className="listItem" key={i}>
            $$dynamic:0
            <Link to={`/$$name$$s/${$$name$$._id}`}>
              <button className="listButton">show</button>
            </Link>
            <Link to={`/$$name$$s/${$$name$$._id}/edit`}>
              <button className="listButton">edit</button>
            </Link>
            <button className="listButton" onClick={() => handleDelete($$name$$._id)}>delete</button>
          </div>
        ))}
        </ul>
      </div>
    )
  }
}
