"use client";

import axios from 'axios'
import styles from './styles.module.css'
import { useState } from 'react'
import Link from 'next/link'

import usePost from '@/hooks/usePost';

export default function RegisterFlow({ handleSubmit, submitError, submitMessage }) {
    const registrationStates = ["email", "name", "username", "password"]
    const [registerState, setRegisterState] = useState(0)

    const [email, setEmail] = useState("");
    const [first, setFirst] = useState("");
    const [last, setLast] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    
    const [clientError, setClientError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleClickSubmit = () => {
        handleSubmit(
            email,
            username,
            first,
            last,
            password
        )
    }

    const validateEmail = (email) => {
        return String(email)
          .toLowerCase()
          .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          );
    }

    const handlePrev = () => {
        setRegisterState(Math.max(0, registerState-1))
    }

    const handleNext = () => {
        setClientError("")
        switch(registrationStates[registerState]) {
            case "email":
                if (email.trim()) 
                    if (validateEmail(email)) {
                        setLoading(true)
                        axios.get(`${process.env.NEXT_PUBLIC_NEUTRINO_IDENTITY_URL}auth/check-email/${email}`)
                            .then((res) => {
                                const { taken } = res.data;
                                if (taken) {
                                    setClientError("an account with this email already exists")
                                } else {
                                    setRegisterState(registerState + 1)
                                }
                            })
                            .catch((err) => setClientError(err))
                            .finally(() => setLoading(false))
                    } else 
                        setClientError("invalid email")
                break;
            case "name":
                if (first.trim() && last.trim()) 
                    setRegisterState(registerState + 1)
                break;
            case "username":
                if (username.trim())
                    setLoading(true)
                    axios.get(`${process.env.NEXT_PUBLIC_NEUTRINO_IDENTITY_URL}auth/check-username/${username}`)
                        .then((res) => {
                            const { taken } = res.data;
                            if (taken) {
                                setClientError("username is already taken")
                            } else {
                                setRegisterState(registerState + 1)
                            }
                        })
                        .catch((err) => setClientError(err))
                        .finally(() => setLoading(false))
                break;
            case "password":
                if (password.trim() && password == confirmPassword)
                    setRegisterState(registerState + 1)
                else
                    setClientError("passwords do not match")
                break;
            default:
                break;
        }
    }


    const getRegisterDisplay = () => {
        switch(registrationStates[registerState]) {
            case "email":
                return (
                    <div className={styles.center}>
                        <div className={styles.listRow}>
                            <code className={styles.label}>email</code>
                        </div>
                        <div className={styles.listRow}>
                            <input 
                                type="text" 
                                className={styles.input} 
                                value={email} 
                                placeholder="email"
                                onChange={(e) => setEmail(e.target.value)} 
                            />
                        </div>
                        <div className={styles.listRow}>
                            <div className="flex-1">
                                <p className='opacity-80 text-sm text-red-400 ml-3'>
                                <code className={styles.code}>{clientError}</code>
                                </p>
                            </div>
                            <button 
                                className={styles.submit} 
                                onClick={(e) => handleNext(e.target.value)} 
                                style={{opacity: email.trim() ? 1 : 0.5, cursor: email.trim() ? "pointer" : "default"}}
                            >
                                {loading ? "......." : "next"}
                            </button>
                        </div>
                    </div>
                )
            case "name":
                return (
                    <div className={styles.center}>
                        <div className={styles.listRow}>
                            <code className={styles.label}>name</code>
                        </div>
                        <div className={styles.listRow}>
                            <input 
                                type="text" 
                                className={styles.input} 
                                style={{marginRight: "1rem"}}
                                value={first} 
                                placeholder="first name"
                                onChange={(e) => setFirst(e.target.value)} 
                            />
                            <input 
                                type="text" 
                                className={styles.input} 
                                value={last} 
                                placeholder="last name"
                                onChange={(e) => setLast(e.target.value)} 
                            />
                        </div>
                        <div className={styles.listRow}>
                            <button 
                                className={styles.previous} 
                                onClick={handlePrev}
                            >
                                prev
                            </button>
                            <div className="flex-1">
                                <p className='opacity-80 text-sm text-red-400 ml-3'>
                                <code className={styles.code}>{clientError}</code>
                                </p>
                            </div>
                            <button 
                                className={styles.submit} 
                                onClick={(e) => handleNext(e.target.value)} 
                                style={{opacity: first.trim() && last.trim() ? 1 : 0.5, cursor: first.trim() && last.trim() ? "pointer" : "default"}}
                            >
                                next
                            </button>
                        </div>
                    </div>
                )
            case "username":
                return (
                    <div className={styles.center}>
                        <div className={styles.listRow}>
                            <code className={styles.label}>username</code>
                        </div>
                        <div className={styles.listRow}>
                            <input 
                                type="text" 
                                className={styles.input} 
                                value={username} 
                                placeholder="username"
                                onChange={(e) => setUsername(e.target.value)} 
                            />
                        </div>
                        <div className={styles.listRow}>
                            <button 
                                className={styles.previous} 
                                onClick={handlePrev}
                            >
                                prev
                            </button>
                            <div className="flex-1">
                                <p className='opacity-80 text-sm text-red-400 ml-3'>
                                <code className={styles.code}>{clientError}</code>
                                </p>
                            </div>
                            <button 
                                className={styles.submit} 
                                onClick={(e) => handleNext(e.target.value)} 
                                style={{
                                    opacity: username.trim() 
                                        ? 1 : 0.5, 
                                    cursor: username.trim() 
                                        ? "pointer" : "default"
                                    }}
                            >
                                {loading ? "......." : "next"}
                            </button>
                        </div>
                    </div>
                )
            case "password":
                return (
                    <div className={styles.center}>
                        <div className={styles.listRow}>
                            <code className={styles.label}>password</code>
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
                            <input 
                                type="password" 
                                className={styles.input} 
                                value={confirmPassword} 
                                placeholder="confirm password"
                                onChange={(e) => setConfirmPassword(e.target.value)} 
                            />
                        </div>
                        <div className={styles.listRow}>
                            <button 
                                className={styles.previous} 
                                onClick={handlePrev}
                            >
                                prev
                            </button>
                            <div className="flex-1">
                                <p className='opacity-80 text-sm text-red-400 ml-3'>
                                <code className={styles.code}>{clientError}{submitError}</code>
                                </p>
                            </div>
                            <button 
                                className={styles.submit} 
                                onClick={handleClickSubmit} 
                                style={{
                                    opacity: password.trim() && password === confirmPassword 
                                        ? 1 : 0.5, 
                                    cursor: password.trim() && password === confirmPassword 
                                        ? "pointer" : "default"
                                    }}
                            >
                                submit
                            </button>
                        </div>
                    </div>
                )
            default:
                break;
        }
    }

    return getRegisterDisplay()
}
