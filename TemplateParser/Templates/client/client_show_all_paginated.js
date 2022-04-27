import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Pagination, Stack } from '@mui/material';
import '../../App.css';

export default function $$Name$$s() {
  const [$$name$$s, set$$Name$$s] = useState([]);
  const [num$$Name$$s, setNum$$Name$$s] = useState(0);
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(5);

  useEffect(() => {
    axios.get("$$LINK$$/$$name$$s/count").then((res) => {
      setNum$$Name$$s(res.data)
    });
    axios.get(`$$LINK$$/$$name$$s?page=${page}&limit=${limit}`).then((res) => {
      set$$Name$$s(res.data)
    });
  }, []);

  useEffect(() => {
    axios.get(`$$LINK$$/$$name$$s?page=${page}&limit=${limit}`).then((res) => {
      set$$Name$$s(res.data)
    });
  }, [page, limit])

  const changePage = (event, value) => {
    setPage(value);
  };

  const changeLimit = (value) => {
    setLimit(parseInt(value))
  }

  function handleDelete(id) {
    axios.delete(`$$LINK$$/$$name$$s/${id}`)
    window.location.reload();
  }

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

      <div className='row center'>
      <Stack spacing={2}>
        <Pagination count={Math.ceil(num$$Name$$s/limit)} page={page} onChange={changePage} />
      </Stack>
      <select value={limit} onChange={(e) => changeLimit(e.target.value)}>
        <option value={"5"}>5</option>
        <option value={"10"}>10</option>
        <option value={"25"}>25</option>
      </select>
      </div>
    </div>
  )
}
