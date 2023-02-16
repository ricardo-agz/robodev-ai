import Image from 'next/image'
import styles from './styles.module.css'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/router';
import Link from 'next/link'

import usePost from '@/hooks/usePost';

export default function Login() {
    const { loading, response, error, postData } = usePost(`${process.env.NEXT_PUBLIC_NEUTRINO_IDENTITY_URL}login`);
    const router = useRouter();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [clientError, setClientError] = useState("");

    const handleSubmit = () => {
        setClientError("")
        if (email && password) {
            postData({
                username: email,
                password
            })
        } else {
            setClientError("please fill out all required fields... ")
        }
    }

    useEffect(() => {
        if (response && response.data.token) {
            localStorage.setItem('jwt', response.data.token)   
            router.push(`/demo`);
        }
    }, [response])

    return (
        <main className={styles.main}>

            <div className={styles.header}>
                <div></div>
                <Link href="/waitlist">
                    <div className="flex items-center cursor-pointer">
                        <div>join waitlist</div>
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
                        className={styles.input} 
                        value={email} 
                        placeholder="username or email"
                        onChange={(e) => setEmail(e.target.value)} 
                    />
                </div>
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
                    <div className="flex-1">
                        <p className='opacity-80 text-sm text-red-400 ml-3'>
                        <code className={styles.code}>{clientError}{error}</code>
                        </p>
                    </div>
                    <button className={styles.submit} onClick={handleSubmit}>
                        {loading ? "loading" : "submit"}
                    </button>
                </div>
            </div>

            <div>
                <p className='mb-8 opacity-60 text-sm'>
                <code className={styles.code}>{"/* yes, this login was built by robodev */"}</code>
                </p>
            </div>

        </main>
    )
}
