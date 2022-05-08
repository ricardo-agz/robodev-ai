import React from 'react';
import '../../App.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Button, ButtonGroup, CircularProgress } from '@mui/material';
import useApi from '../../hooks/useApi';
$$AUTH_IMPORTS$$
import configData from '../../../config.json'

export default function $$Name$$s() {
  const { result: <$= camel_case(self.model.plural) $>, loading, error, refresh } = useApi(`${configData.SERVER_URL}/$$pluralname$$`);
  const navigate = useNavigate();

  function handleDelete(id) {
    axios.delete(`${configData.SERVER_URL}/$$name$$/${id}`$$header$$);
    window.location.reload();
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (loading || !<$= camel_case(self.model.plural) $>) {
    return <CircularProgress />;
  } else {
    return (
      <div className='container'>
        <h1><$= title_space_case(self.model.plural) $></h1>
        <Button 
          variant={"contained"}
          onClick={() => navigate("/$$pluralname$$/new")}
        >
        New <$= title_space_case(self.model.name) $>
        </Button>

        <ul>
        {<$= camel_case(self.model.plural) $>.map(($$nameCamel$$, i) => (
          <div className="listItem" key={i}>
            <$= f"<li key={{i}}>{{{camel_case(self.model.name)}.{self.model.schema[0]['name']}}}</li>" $>
            <ButtonGroup variant="outlined" size="small">
              <Button onClick={() => navigate(`/$$name$$/${$$name$$._id}`)}>show</Button>
              <Button onClick={() => navigate(`/$$name$$/${$$name$$._id}/edit`)}>edit</Button>
              <Button color="error" onClick={() => handleDelete($$name$$._id)}>delete</Button>
            </ButtonGroup>
          </div>
        ))}
        </ul>
      </div>
    );
  };
};
