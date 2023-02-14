"use client";

import Image from 'next/image'
import { Inter } from '@next/font/google'
import styles from './page.module.css'
import { useState } from 'react'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export default function Home() {
    const [accessCode, setAccessCode] = useState("");


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
                <p className='mb-8 opacity-60'>
                an AI chatbot that converts natural language into full backend web applications
                </p>
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
                <p className='mt-4 opacity-60 text-left w-full'>
                DM &nbsp;
                <code className={styles.code}><a href="https://twitter.com/ricardo_agzz" target="_blank" rel="noreferrer noopener">@ricardo_agzz</a></code>&nbsp;
                on Twitter to get access <br/>
                <span className='text-xs'>(or join the <Link href="/waitlist" className='underline'>waitlist</Link> if you don't have twitter)</span>
                
                </p>
            </div>

            <div>
                <p className='mb-8 opacity-60 text-sm'>
                <code className={styles.code}>{"/* yes, this waitlist was built by robodev */"}</code>
                </p>
            </div>

        </main>
    )
}
