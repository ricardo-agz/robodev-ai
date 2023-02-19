import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Link from 'next/link'
import Image from 'next/image'
import styles from './styles.module.css'
import axios from 'axios'
import useLocalstorage from '../hooks/useLocalStorage'
import FolderDisplay from '../components/folderDisplay'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dark } from 'react-syntax-highlighter/dist/cjs/styles/prism';

import usePost from '@/hooks/usePost'

function getQueryString(str) {
    const index = str.indexOf('?');
    return index === -1 ? '' : str.slice(index + 1);
}

export default function ViewProject() {
    const router = useRouter();
    const { asPath } = router;
    const [buildfile, setBuildfile] = useLocalstorage("buildfile", null);
    const [code, setCode] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { 
        loading: exportLoading, 
        response: exportResponse, 
        error: exportError, 
        postData: exportPost 
    } = usePost(`${process.env.NEXT_PUBLIC_NEUTRINO_GENERATOR_URL}generator`);

    // check for authentication
    useEffect(() => {
        const jwt = localStorage.getItem('jwt')
        if (!jwt) {
            router.push('/login')
        }
    }, [])

    useEffect(() => {
        let cancelled = false;
        let queryString = getQueryString(asPath)
        
        setLoading(true);
        axios.put(`${process.env.NEXT_PUBLIC_NEUTRINO_GENERATOR_URL}previewpage?${queryString}`, buildfile)
            .then((r) => {
                if (!cancelled) {
                    setCode(r.data.content);
                    setLoading(false);
                    setError(null);
                }
            })
            .catch((e) => {
                let errMessage = e.response && e.response.data.message 
                    ? e.response.data.message 
                    : e.message
                setLoading(false);
                setError(errMessage);
            });

        return () => {
            cancelled = true;
        };
    }, [asPath]);


    const exportProject = () => {
        exportPost(buildfile)
    }

    useEffect(() => {
        if (exportResponse)
            downloadZipFile(exportResponse.data)
    }, [exportResponse])


    return (
        <div className='flex flex-col' style={{width: "100vw", height: "100vh", overflowY: "scroll"}}>
            <div className='flex items-center p-10' style={{height: "10vh"}}>
                <div className='flex-1'/>
                <p className='opacity-80 text-sm text-red-400 ml-3 mr-6'>
                    <code className={styles.code}>{exportError}</code>
                </p>
                <button className={styles.button} onClick={() => {router.push("/demo")}}>
                    back
                </button>
                <button className={styles.thirteen} style={{width: "5rem"}} onClick={exportProject}>
                    {exportLoading 
                        ? "loading" 
                        : "export"}
                </button>
            </div>
            <div className='flex flex-1 flex-col md:flex-row lg:flex-row' style={{height: "80vh", overflowY: "scrollx"}}>
                <div 
                    className='m-3 p-3 block md:block lg:block' 
                    style={{flex: 1, borderRadius: "0.5rem", border: "1px solid #ffffff50"}}
                >
                    <FolderDisplay buildfile={buildfile}/>
                </div>
                <div className='m-3' style={{flex: 3, borderRadius: "0.5rem", backgroundColor: "#000", maxHeight: "80vh", overflowY: "scroll", border: "1px solid #ffffff50"}}>
                    <SyntaxHighlighter 
                            language="javascript" 
                            style={dark} 
                            customStyle={{
                                backgroundColor: '#000',
                                flex: 1,
                                textAlign: 'left',
                                borderWidth: 0,
                                overflowY: 'scroll',
                                fontSize: '.8em',
                                margin: '1em',
                                marginRight: 0,
                                padding: '2em',
                                border: "none",
                                boxShadow: "none",
                            }}
                        >
                            {loading
                                ? '/ loading... /'
                                : error
                                    ? `/ error previewing page: ${error} /`
                                    : code
                            }
                    </SyntaxHighlighter> 
                </div>
            </div>
            <div className='flex items-center pr-5' style={{height: "10vh"}}>
                <div style={{flex: 1}}/>
                <div className="flex items-center cursor-pointer" onClick={() => {router.push("/")}}>
                    <div className={styles.thirteen}>
                        <Image src="/logowhite.svg" alt="13" width={40} height={31} priority />
                    </div>
                </div>
            </div>
        </div>
    )
}

const downloadZipFile = (data) => {
    const element = document.createElement('a');
    const file = new Blob([data], {type: 'application/octet-stream'});
    element.href = URL.createObjectURL(file);
    element.download = `neutrinoproject.zip`;
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
};
