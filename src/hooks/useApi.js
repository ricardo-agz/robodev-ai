import { useState, useEffect } from 'react';
import axios from 'axios';

function useApi(url) {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [data, setData] = useState(null);

    const fetchData = async () => {
        setLoading(true);
        axios.get(url)
            .then((res) => {
                setData(res.data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    };

    useEffect(() => {
        fetchData();
    }, [url]);

    const refresh = () => {
        fetchData();
    };

    return { loading, error, data, refresh };
}

export default useApi;
