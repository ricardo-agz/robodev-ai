import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link'
import Image from 'next/image'
import axios from 'axios';
import styles from './styles.module.css'
import RegisterFlow from '@/components/registerFlow';

export default function AccessCode({ verified, message }) {
    const [accessCode, setAccessCode] = useState('');
    const [loading, setLoading] = useState(false);
    const [registerErr, setRegisterErr] = useState(null);
    const router = useRouter();

    useEffect(() => {
        const jwt = localStorage.getItem('jwt')
        if (jwt) {
            router.push('/demo')
        }
    }, [])

    const handleAccessCodeSubmit = async (e) => {
        e.preventDefault();
        router.push(`/access?accessCode=${accessCode}`);
    };

    const handleRegisterSubmit = async (email, username, first, last, password) => {
        setLoading(true)
        setRegisterErr(null)

        console.log("submitting...")

        axios.post(`${process.env.NEXT_PUBLIC_NEUTRINO_IDENTITY_URL}register`, { 
            email,
            username, 
            firstName: first,
            lastname: last,
            password,
            accessCode
        })
            .then(res => {
                // Store the JWT in local storage or a cookie
                if (res.data.token) 
                    localStorage.setItem('jwt', res.data.token)   
                    router.push(`/demo`);
            })
            .catch(err => {
                setRegisterErr(err.response.data.message ? err.response.data.message : "server error...")
                console.log("error submitting...")
                console.log(err)
            })
            
            .finally(() => {
                setLoading(false)
            })
  }


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

            { verified ?
                <RegisterFlow 
                    handleSubmit={(email, username, first, last, password) => handleRegisterSubmit(email, username, first, last, password)}
                    submitError={registerErr}
                />
            :
            <div className={styles.center}>
                <div className={styles.listRow}>
                    <input 
                        type="text" 
                        className={styles.input} 
                        value={accessCode} 
                        placeholder="access code"
                        onChange={(e) => setAccessCode(e.target.value)} 
                    />
                </div>
                <div className={styles.listRow}>
                    <div className="flex-1">
                        <p className='opacity-80 text-sm text-red-400 ml-3'>
                        <code className={styles.code}>{message}</code>
                        </p>
                    </div>
                    <button className={styles.submit} onClick={handleAccessCodeSubmit}>
                        {loading ? "loading" : "submit"}
                    </button>
                </div>
            </div>
            }

            

            <div>
                <p className='mb-8 opacity-60 text-sm'>
                <code className={styles.code}>{"/* yes, this login was built with AI */"}</code>
                </p>
            </div>

        </main>
  );
}

export async function getServerSideProps(context) {
    const { accessCode } = context.query;
    let verified = false;
    let message = ""
    let url = `${process.env.NEXT_PUBLIC_NEUTRINO_IDENTITY_URL}waitlist/accesscode/${accessCode}/verify`

    if (accessCode) {
        await axios.post(url, {})
            .then((res) => {
                verified = res.data.verified
                if (!verified) {
                    message = "invalid access code"
                }
            })
            .catch((e) => {
                message = e.response && e.response.data.message 
                    ? e.response.data.message 
                    : e.message
            })
    }

    return {
        props: {
            verified,
            message,
        },
    };
}
