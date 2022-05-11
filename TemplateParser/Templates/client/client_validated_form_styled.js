import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom';
import MuiAlert from '@mui/material/Alert';
import {
  Snackbar,
  TextField,
  Button,
  Checkbox,
  Stack
} from '@mui/material'

const Alert = React.forwardRef((props, ref) => {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

export default function ValidatedForm(props) {
  <$= "const {{ id }} = useParams();" if len(self.model.belongs_to) > 0 else "" $>
  $$USE_STATES$$
  const [err, setErr] = useState(null)
  const [openErr, setOpenErr] = useState(false)

  useEffect(() => {
		if (props.model) {
			<$ for param in self.model.schema $>
      <$= f"set{camel_case(param['name'])}(props.model.{param['name']});" $>
      <$ end $>
		}
	}, [props.model]);

  const validate = () => {
    $$dynamic:1
      setOpenErr(true)
    }
  }

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenErr(false);
  };

  return (
    <div className='container'>
      <Stack spacing={3}>
        $$dynamic:2
        <Button variant="contained" onClick={validate}>Submit</Button>
      </Stack>

      <Snackbar open={openErr} autoHideDuration={6000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
          {err}
        </Alert>
      </Snackbar>
    </div>
  )
}