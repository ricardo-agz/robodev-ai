import Image from 'next/image'
import styles from './styles.module.css'
import { useState } from 'react'
import Link from 'next/link'

import usePost from '@/hooks/usePost';
import AdminDashboard from '@/components/adminDashboard';
import AdminLogin from '@/components/adminLogin';



export default function Admin() {
    const [loggedIn, setLoggedIn] = useState(false);

    return (
        <main className={loggedIn ? styles.dashboardMain : styles.main}>

            <div className={styles.header}>
                <div></div>
                <Link href="/">
                    <div className="flex items-center cursor-pointer">
                        <div>home</div>
                        <div className={styles.thirteen}>
                            <Image src="/logowhite.svg" alt="13" width={40} height={31} priority />
                        </div>
                    </div>
                </Link>
            </div>

            {loggedIn 
                ? <AdminDashboard /> 
                : <AdminLogin setLoggedIn={(val) => setLoggedIn(val)}/> 
            }

            <div/>
        </main>
    )
}
