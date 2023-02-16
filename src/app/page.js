"use client";

import Image from 'next/image'
import { Inter } from '@next/font/google'
import styles from './page.module.css'
import { useState } from 'react'
import Link from 'next/link'
import DemoPreview from '@/components/demoPreview';

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

            <DemoPreview/>

            <div>
                <p className='mb-8 opacity-60 text-sm'>
                <code className={styles.code}>
                    {"/* "} 
                    or message &nbsp;
                    <a href="https://twitter.com/ricardo_agzz" target="_blank" rel="noreferrer noopener">@ricardo_agzz</a>&nbsp;
                    on Twitter to get access                
                    {" */"}
                </code>
                </p>
            </div>

        </main>
    )
}
