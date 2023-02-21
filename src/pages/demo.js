import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import Link from 'next/link'
import Image from 'next/image'
import styles from './styles.module.css'
import axios from 'axios'
import useLocalstorage from '../hooks/useLocalStorage'

const initMessages = [
    "hey! i'm newt, the neutrino AI", 
    "i can code you the backend for your web app with just a description", 
    "what type of app would you like to build today?"
]

const textboxPlaceholder = "I want to build a twitter-style social media app where users can create posts, comment and like posts, follow other users, and retweet posts..."

export default function Demo() {
    const router = useRouter();
    const [appDescription, setAppDescription] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [messages, setMessages] = useState(initMessages.slice(0,1))
    const [buildfile, setBuildfile] = useLocalstorage("buildfile", null);
    const [showViewButton, setShowViewButton] = useState(false);

    useEffect(() => {
        if (buildfile)
            setShowViewButton(true)
    }, [])

    useEffect(() => {
        setShowViewButton(buildfile ? true : false)
    }, [buildfile])

    // check for authentication
    useEffect(() => {
        const jwt = localStorage.getItem('jwt')
        const userId = localStorage.getItem('user')
        if (!jwt || !userId) {
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


    const pollForTaskCompletion = async (jobId) => {
        await axios.get(`${process.env.NEXT_PUBLIC_NEUTRINO_GENERATOR_URL}check-ai-task/${jobId}`)
            .then((res) => {
                if (res.status === 200) {
                    // Task is done, console.log the response
                    let arr = JSON.parse(JSON.stringify(messages))
                    let m = "done! click on 'view project' to view your code"
                    arr.push(m)
                    setMessages(arr)
                    // downloadZipFile(res.data.data);
                    setBuildfile(res.data.buildfile)
                    setLoading(false);
                  } else if (res.status === 202) {
                    // Task is still running, poll again after 10 seconds
                    let status = res.data.message

                    // Adding a new message if the job is at a new status point
                    if (status !== messages[messages.length-1]) {
                        let arr = JSON.parse(JSON.stringify(messages))
                        arr.push(status)
                        setMessages(arr)
                        console.log(arr)
                    }

                    setTimeout(() => pollForTaskCompletion(jobId), 5000);
                  } else {
                    // An error occurred, console.log the error message
                    console.error(res.data.message);
                    setLoading(false);
                  }
            })
            .catch((e) => {
                // An error occurred, console.log the error message
                let errMessage = e.response && e.response.data.message 
                    ? e.response.data.message 
                    : e.message
                setError(errMessage)
                setLoading(false);
            })
    }

    const handleSubmit = async () => {
        if (loading)
            return;

        setShowViewButton(false);

        setLoading(true);
        setError(null);
        let arr = JSON.parse(JSON.stringify(messages))
        let m = "sounds great! give me a minute or two to design and build your app..."
        arr.push(m)
        setMessages(arr)

        const userId = localStorage.getItem('user')

        // Enqueue the task
        const response = await axios.post(
            `${process.env.NEXT_PUBLIC_NEUTRINO_GENERATOR_URL}enqueue-ai-task`, 
            { 
                description: appDescription,
                user: userId
            }
        )
            .then((res) => {
                pollForTaskCompletion(res.data.job_id);
            })
            .catch((e) => {
                setLoading(false);
                let errMessage = e.response && e.response.data.message 
                    ? e.response.data.message 
                    : e.message
                setError(errMessage)
            })
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
                    {showViewButton &&
                    <button className={styles.submit} style={{marginLeft: 0}} onClick={() => router.push("/viewProject?page=server-file")}>
                        view project
                    </button>
                    }
                    <div className="flex-1">
                        <p className='opacity-80 text-sm text-red-400 ml-3'>
                        <code className={styles.code}>{error}</code>
                        </p>
                    </div>
                    <button className={styles.submit} onClick={handleSubmit}>
                        {loading ? "loading..." : "submit"}
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