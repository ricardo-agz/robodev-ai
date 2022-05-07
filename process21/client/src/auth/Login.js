import React, { useState } from 'react'
import { Button, TextField, Stack } from '@mui/material';
import useAuth from '../hooks/useAuth'

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login, error } = useAuth();

  return (
    <div className='col'>
      <h1>Login</h1>
      <Stack spacing={3}>
        {error &&
          <div style={{color: "red"}}>{error}</div>
        }
        <TextField
          label="username"
          onChange={(e)=>setUsername(e.target.value)}
          size="small"
        />
        <TextField
          label="password"
          onChange={(e)=>setPassword(e.target.value)}
          type={"password"}
          size="small"
        />
        {/* Submit */}
        <Button 
          variant="contained" 
          onClick={() => login(username, password)}
        >Login</Button>
      </Stack>
    </div>
  )
}