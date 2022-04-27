import React, { useState, useEffect } from "react";
import axios from 'axios';
$$AUTH:0

export default function useApi(url) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(false);
  const [error, setError] = useState();
  const [refreshIndex, setRefreshIndex] = useState(0);

  const refresh = () => {
    setRefreshIndex(refreshIndex + 1);
  };
  
  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    axios.get(url$$header$$)
    .then(r => {
      if (!cancelled) {
        setResult(r.data);
        setLoading(false);
      };
    })
    .catch(err => {
      setError(err.response.data);
    })
    return () => {
      cancelled = true;
    };
  }, [url, refreshIndex]);

  return {
    result, 
    loading,
    error,
    refresh
  };
}