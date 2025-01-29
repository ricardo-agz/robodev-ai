import { useState } from 'react';
import axios from 'axios';

export default function usePost(url) {
    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    function replaceId(substring, id) {
        return substring.replace(':id', id);
    }

    const postData = async (data, id=null) => {
        let parsedUrl = url;
        if (id) {
            parsedUrl = replaceId(url, id)
        }

        setLoading(true)
        setError(null)

        await axios.post(parsedUrl, data)
            .then((res) => {
                setResponse(res)
                setLoading(false)
            })
            .catch((e) => {
                let errMessage = e.response && e.response.data.message 
                    ? e.response.data.message 
                    : e.message
                setError(errMessage);
                setLoading(false);
            })
    }   

    return { loading, response, error, postData };
}
