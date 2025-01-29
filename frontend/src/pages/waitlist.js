"use client";

import Image from 'next/image'
import { Inter } from '@next/font/google'
import styles from './styles.module.css'
import { useState } from 'react'
import Link from 'next/link'

import usePost from '../hooks/usePost'

const inter = Inter({ subsets: ['latin'] })

export default function Waitlist() {
    const { loading, response, error, postData } = usePost(`${process.env.NEXT_PUBLIC_NEUTRINO_IDENTITY_URL}waitlist/apply`);

    const [first, setFirst] = useState("");
    const [last, setlast] = useState("");
    const [email, setEmail] = useState("");
    const [company, setCompany] = useState("");
    const [primaryUse, setPrimaryUse] = useState("");
    const [useDescription, setuseDescription] = useState("");
    const [clientError, setClientError] = useState("")

    const handleOptionChange = (e) => {
        setPrimaryUse(e.target.value);
    };

    const handleSubmit = () => {
        setClientError("")
        if (first && last && email && primaryUse && useDescription) {
            postData({
                first,
                last,
                email,
                company,
                primaryUse,
                useDescription
            })
        } else {
            setClientError("please fill out all required fields... ")
        }
    }

    return (
        <main className={styles.main}>

            <div className={styles.header}>
                <div></div>
                <Link href="/login">
                    <div className="flex items-center cursor-pointer">
                        <div>log in</div>
                        <div className={styles.thirteen}>
                            <Image src="/logowhite.svg" alt="13" width={40} height={31} priority />
                        </div>
                    </div>
                </Link>
            </div>

            <div className={styles.center}>
                <div className={styles.listRow}>
                    <input 
                        type="text" 
                        style={{marginRight: "1rem"}}
                        className={styles.input} 
                        value={first} 
                        placeholder="first name*"
                        onChange={(e) => setFirst(e.target.value)} 
                    />
                    <input 
                        type="text" 
                        className={styles.input} 
                        value={last} 
                        placeholder="last name*"
                        onChange={(e) => setlast(e.target.value)} 
                    />
                </div>

                <div className={styles.listRow}>
                    <input 
                        type="text" 
                        className={styles.input} 
                        value={email} 
                        placeholder="email*"
                        onChange={(e) => setEmail(e.target.value)} 
                    />
                </div>

                <div className={styles.listRow}>
                    <input 
                        type="text" 
                        className={styles.input} 
                        value={company} 
                        placeholder="company name"
                        onChange={(e) => setCompany(e.target.value)} 
                    />  
                </div>
            
                <div className={styles.listRow}>
                    <p className='opacity-60 text-sm flex-1 ml-3'>
                        <code className={styles.codeLabel}>how do you primarily plan to use neutrino?*</code>
                    </p>
                    <select 
                        id="options" value={primaryUse} 
                        onChange={handleOptionChange} 
                        className={styles.input}
                        placeholder="primary use case"
                    >
                        <option value="">Select*</option>
                        <option value="building new product">Building a new product</option>
                        <option value="integrating into existing product">Integrating into an existing product</option>
                        <option value="academia">Academic purposes</option>
                        <option value="experimenting">Just trying it out</option>
                        <option value="other">Other</option>
                    </select>
                </div>

                <div className={styles.listRow}>
                    <textarea 
                        type="text" 
                        className={styles.textarea} 
                        value={useDescription} 
                        placeholder="any ideas you're specifically planning on building with neutrino?*"
                        onChange={(e) => setuseDescription(e.target.value)} 
                    />
                </div>
                
                <div className={styles.listRow}>
                    <div className="flex flex-1">
                        <p className='opacity-80 text-sm text-red-400 ml-3'>
                        <code className={styles.code}>{clientError}{error}</code>
                        </p>
                        <p className='opacity-90 text-sm text-green-600 ml-3'>
                        <code className={styles.code}>{response ? response.data.message : ""}</code>
                        </p>
                    </div>
                    <button className={styles.submit} onClick={handleSubmit}>
                        {loading ? "loading" : "submit"}
                    </button>
                </div>
            </div>

            <div>
                <p className='mb-8 opacity-60 text-sm'>
                <code className={styles.code}>{"/* yes, this application was built with AI */"}</code>
                </p>
            </div>

        </main>
    )
}
