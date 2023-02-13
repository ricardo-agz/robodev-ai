"use client";

import Image from 'next/image'
import { Inter } from '@next/font/google'
import styles from './styles.module.css'
import { useState } from 'react'

const inter = Inter({ subsets: ['latin'] })

export default function Home() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");


    return (
        <main className={styles.main}>

            <div className={styles.header}>
                <div></div>
                <div className="flex items-center cursor-pointer">
                    <div>join waitlist</div>
                    <div className={styles.thirteen}>
                        <Image src="/logowhite.svg" alt="13" width={40} height={31} priority />
                    </div>
                </div>
            </div>

            <div className={styles.center}>
                <input 
                    type="text" 
                    className={styles.input} 
                    value={email} 
                    placeholder="username or email"
                    onChange={(e) => setEmail(e.target.value)} 
                />
                <div className={styles.description}>
                    <input 
                        type="password" 
                        className={styles.input} 
                        value={password} 
                        placeholder="password"
                        onChange={(e) => setPassword(e.target.value)} 
                    />
                    <div className={styles.enter}>
                        <p>enter</p>
                    </div>
                </div>
            </div>

            <div>
                <p className='mb-8 opacity-60 text-sm'>
                <code className={styles.code}>/* yes, this login was built by robodev */</code>
                </p>
            </div>

        </main>
    )
}
