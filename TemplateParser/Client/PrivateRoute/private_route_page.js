import React, { useContext, useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { $$Name$$Context } from '../hooks/$$Name$$Context';

export default function PrivateRoute({ component }) {
  const [loading, setLoading] = useState(true);
  const { auth$$Name$$ } = useContext($$Name$$Context);

  useEffect(() => {
    setLoading(false)
  }, [auth$$Name$$])

  if (auth$$Name$$) return component
  else if (loading) return <div>loading ...</div>
  else return <Navigate to="/login" />
}