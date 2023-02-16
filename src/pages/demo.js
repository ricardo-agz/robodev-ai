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

export default function Demo() {
  const router = useRouter()
  const [appDescription, setAppDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [messages, setMessages] = useState(initMessages.slice(0,1))

  // check for authentication
  useEffect(() => {
    const jwt = localStorage.getItem('jwt')
    if (!jwt) {
      router.push('/login')
    }
  }, [])

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

  const handleSubmit = () => {

  }

  const handleLogout = () => {
    localStorage.removeItem('jwt')
  }

  return (
    <main className={styles.main}>

        <div className={styles.header}>
            <div></div>
            <Link href="/login">
                <div className="flex items-center cursor-pointer" onClick={handleLogout}>
                    <div>log out</div>
                    <div className={styles.thirteen}>
                        <Image src="/logowhite.svg" alt="13" width={40} height={31} priority />
                    </div>
                </div>
            </Link>
        </div>

        

        <div className={styles.center}>
            <div className={styles.listRow} style={{height: "3rem", alignItems: 'flex-end'}}>
                <Image src="/newt_profile.jpg" alt="13" width={60} height={60} style={{borderRadius: "5rem", border: "3px solid white"}} priority />
                <div className={styles.messageContainer}>
                    { messages.map((m, i) => (
                        <code 
                            key={m}
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
                    <p className='opacity-80 text-sm text-red-400 ml-3'>
                    <code className={styles.code}>{error}</code>
                    </p>
                </div>
                <button className={styles.submit} onClick={handleSubmit}>
                    {loading ? "loading" : "submit"}
                </button>
            </div>
        </div>

        <div>
            <p className='mb-8 opacity-60 text-sm'>
            <code className={styles.code}></code>
            </p>
        </div>

    </main>
)
}