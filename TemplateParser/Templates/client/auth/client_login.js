import React, { useState } from 'react'
import useAuth from '../hooks/useAuth'

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login, error } = useAuth();

  return (
    <div>
      <h1>Login</h1>
      {error &&
        <div style={{color: "red"}}>{error}</div>
      }

      <label>username</label>
      <input 
        type="text" 
        onChange={(e) => setUsername(e.target.value)}
      /><br/>
      <label>password</label>
      <input 
        type="password" 
        onChange={(e)=>setPassword(e.target.value)}
      /><br/>

      {/* Submit */}
      <button onClick={() => login(username, password)}>login</button>
    </div>
  )
}