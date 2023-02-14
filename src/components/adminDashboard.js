"use client";

import Image from 'next/image'
import styles from './styles.module.css'
import { useEffect, useState } from 'react'
import Link from 'next/link'

import useApi from '@/hooks/useApi';
import usePost from '@/hooks/usePost';

import React from 'react';

function TableRow({ rowData, handleApprove }) {
    const [row, setRow] = useState(rowData);
    useEffect(() => {
        setRow(rowData)
    }, [rowData])

    return (
        <tr key={row._id} className="flex-1">
            
            
            <td className={styles.tableCell}>{row ? `${row.first} ${row.last}` : ""}</td>
            <td className={styles.tableCell}>{row ? row.email : ""}</td>
            <td className={styles.tableCell}>{row ? row.company : ""}</td>
            <td className={styles.tableCell}>{row ? row.primaryUse : ""}</td>
            <td className={styles.tableCell}>{row ? row.useDescription : ""}</td>
            <td className={styles.tableCell}>{row ? row.approved : ""}</td>
            <td className={styles.tableCell}>
                {
                    row.approved != "true" ?
                    <button
                        className='underline'
                        onClick={() => handleApprove(row._id)}
                    >approve</button>
                    : "approved"
                }
            </td>
            
        </tr>
    );
}

function Table({ data, handleApprove }) {
    const [rows, setRows] = useState(data);
    useEffect(() => {
        setRows(data)
    }, [data])

    return (
      <table key={"table"} className="w-full">
        <thead>
          <tr>
            <th className={styles.tableCol}>Name</th>
            <th className={styles.tableCol}>Email</th>
            <th className={styles.tableCol}>Company</th>
            <th className={styles.tableCol}>Primary Use</th>
            <th className={styles.tableCol}>Use Description</th>
            <th className={styles.tableCol}>Approved</th>
            <th className={styles.tableCol}>Approve</th>
          </tr>
        </thead>
        <tbody>
        {rows 
            ? rows.map((app) => (
                <TableRow rowData={app} key={app._id} handleApprove={(id) => handleApprove(id)} />
            ))
            : "no items"
        }
        </tbody>
      </table>
    );
  }



export default function AdminDashboard() {
    const { loading, error, data, refresh } = useApi(`${process.env.NEXT_PUBLIC_NEUTRINO_IDENTITY_URL}waitlist`);
    const { loading: codeLoading, response: codeResponse, error: codeError, postData: postCreateCode } = usePost(`${process.env.NEXT_PUBLIC_NEUTRINO_IDENTITY_URL}waitlist/accesscode`);
    const { loading: approveLoading, response: responseLoading, error: errorLoading, postData: approveApp } = usePost(`${process.env.NEXT_PUBLIC_NEUTRINO_IDENTITY_URL}waitlist/approve/:id`);

    const [accessCode, setAccessCode] = useState(null)

    const [applications, setApplications] = useState([])
    useEffect(() => {
        if (data) {
            setApplications(data ? data : [])
            console.log(data)
        }
    }, [data])

    const generateAccessCode = () => {
        postCreateCode()
    }
    useEffect(() => {
        if (codeResponse) {
            setAccessCode(codeResponse.data.code.code)
        }
    }, [codeResponse])

    const handleApprove = (id) => {
        approveApp({}, id)
    }

    return (
        <div className={styles.center}>
            <div className='w-full'>
                <div className='flex items-center w-full mb-4'>
                    <h2 className='flex-1'>generate access code</h2>
                    <p>{ accessCode ? accessCode : ""} { codeError ? codeError : ""}</p>
                    <button
                        onClick={generateAccessCode}
                        className={styles.submit}
                    >
                        { codeLoading ? "loading" : "generate"}
                    </button>
                </div>
                
            </div>

            <div className='w-full mt-8'>
                <div className='flex items-center w-full mb-4'>
                    <h2 className='flex-1'>waitlist applications</h2>
                    <button
                        onClick={refresh}
                        className={styles.submit}
                    >
                        { loading ? "loading" : "refresh"}
                    </button>
                </div>
                
                <Table data={applications} handleApprove={(id) => handleApprove(id)}/>
            </div>
            
        </div>
    )
}
