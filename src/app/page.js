"use client";

import Image from 'next/image'
import { Inter } from '@next/font/google'
import styles from './page.module.css'
import { useState } from 'react'

const inter = Inter({ subsets: ['latin'] })

export default function Home() {
    const [accessCode, setAccessCode] = useState("");


    return (
        <main className={styles.main}>

            <div className={styles.header}>
                <div></div>
                <div className="flex items-center cursor-pointer">
                    <div>log in</div>
                    <div className={styles.thirteen}>
                        <Image src="/logowhite.svg" alt="13" width={40} height={31} priority />
                    </div>
                </div>
            </div>

            <div className={styles.center}>
                <div className={styles.description}>
                    <input 
                        type="text" 
                        className={styles.input} 
                        value={accessCode} 
                        placeholder="access code"
                        onChange={(e) => setAccessCode(e.target.value)} 
                    />
                    <div className={styles.enter}>
                        <p>enter</p>
                    </div>
                </div>
                <p className='mt-4 opacity-60'>
                DM &nbsp;
                <code className={styles.code}><a href="https://twitter.com/ricardo_agzz" target="_blank">@ricardo_agzz</a></code>&nbsp;
                on Twitter to get access
                </p>
            </div>

            <div>

            </div>

        </main>
    )
}
