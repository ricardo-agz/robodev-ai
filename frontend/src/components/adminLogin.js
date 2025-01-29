"use client"

import Image from 'next/image'
import styles from './styles.module.css'
import { useEffect, useState } from 'react'
import Link from 'next/link'

import usePost from '@/hooks/usePost';



export default function AdminLogin({ setLoggedIn }) {
    const { loading, response, error, postData } = usePost(`api/admin`);

    const [password, setPassword] = useState("");
    const [clientError, setClientError] = useState("");

    const handleSubmit = (e) => {
        console.log("bruh")
        e.preventDefault()
        setClientError("")
        if (password) {
            postData({ password })
        } else {
            setClientError("please fill out all required fields... ")
        }
    }

    useEffect(() => {
        setLoggedIn(response);
    }, [response])

    return (
        <form className={styles.center}>
            <div className={styles.listRow}>
                <input 
                    type="password" 
                    className={styles.input} 
                    value={password} 
                    placeholder="password"
                    onChange={(e) => setPassword(e.target.value)} 
                />
            </div>
            <div className={styles.listRow}>
                <div className="flex flex-1">
                    <p className='opacity-80 text-sm text-red-400 ml-3'>
                    <code className={styles.code}>{clientError}{error}</code>
                    </p>
                </div>
                <div className="flex flex-1">
                    <p className='opacity-80 text-sm text-green-600 ml-3 text-left'>
                    <code className={styles.code}>{response ? response.data.message : ""}</code>
                    </p>
                </div>
                <button className={styles.submit} type="button" onClick={handleSubmit}>
                    {loading ? "loading" : "submit"}
                </button>
            </div>
        </form>
    )
}
