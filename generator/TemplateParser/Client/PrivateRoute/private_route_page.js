import React, { useContext, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { CircularProgress } from '@mui/material';
import { $$Name$$Context } from '../hooks/$$Name$$Context';

export default function PrivateRoute({ component }) {
  const [loading, setLoading] = useState(true);
  const { auth$$Name$$, authLoading } = useContext($$Name$$Context);

  if (auth$$Name$$) return component
  else if (authLoading) return <CircularProgress />;
  else return <Navigate to="/login" />
}