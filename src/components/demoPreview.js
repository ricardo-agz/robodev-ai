"use client"

import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Link from 'next/link'
import Image from 'next/image'
import styles from './styles.module.css'

const initMessages = [
    "hey! i'm newt, the neutrino AI", 
    "i can help you build a backend for your web app with just a description", 
    "what type of app would you like to build today?"
]

const textboxPlaceholder = "I want to build a twitter-style social media app where users can create posts, comment and like posts, follow other users, and retweet posts..."

export default function DemoPreview() {
  const [appDescription, setAppDescription] = useState("");
  const [messages, setMessages] = useState(initMessages.slice(0,1))

  // push message after x seconds
  useEffect(() => {
    const timer = setTimeout(() => {
        setMessages(initMessages.slice(0, 2))
    }, 4000)

    const secondTimer = setTimeout(() => {
        setMessages(initMessages.slice(0, 3))
    }, 8000)

    // cleanup function to clear the timer if the component unmounts before the timer expires
    return () => {
        clearTimeout(timer)
        clearTimeout(secondTimer)
    }
  }, [])


  return (
        <div className={styles.center}>
            <div className={styles.listRow} style={{height: "3rem", alignItems: 'flex-end'}}>
                <Image src="/newt_profile.jpg" alt="13" width={60} height={60} style={{borderRadius: "5rem", border: "3px solid white"}} priority />
                <div className={styles.messageContainer}>
                    { messages.map((m, i) => (
                        <code 
                            className={styles.aiText} 
                            style={{opacity: i === messages.length-1 ? 1 : .5, marginBottom: 20}}
                        >{m}</code>
                    ))}
                </div>
            </div>
            <div className={styles.listRow}>
                <textarea 
                    type="text" 
                    className={styles.textarea} 
                    value={appDescription} 
                    placeholder={textboxPlaceholder}
                    onChange={(e) => setAppDescription(e.target.value)} 
                />
            </div>
            <div className={styles.listRow}>
                <div className="flex-1">
                    {/* <p className='opacity-80 text-xs ml-3'>
                        <code className={styles.code}>(newt will code the backend for a twitter-like app...)</code>
                    </p> */}
                </div>
                <Link href="/login">
                    <button className={styles.button}>
                        log in
                    </button>
                </Link>
                <Link href="/waitlist">
                    <button className={styles.button}>
                        join waitlist
                    </button>
                </Link>
            </div>
        </div>
    )
}