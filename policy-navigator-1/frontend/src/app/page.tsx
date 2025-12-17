import React from 'react';
import Link from 'next/link';

const HomePage = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen">
            <h1 className="text-4xl font-bold mb-4">Welcome to Policy Navigator</h1>
            <p className="mb-8">A multi-agent AI system for government policy interpretation, eligibility verification, and benefit matching.</p>
            <div className="flex space-x-4">
                <Link href="/policies">
                    <a className="bg-blue-500 text-white px-4 py-2 rounded">Interpret Policies</a>
                </Link>
                <Link href="/eligibility">
                    <a className="bg-green-500 text-white px-4 py-2 rounded">Check Eligibility</a>
                </Link>
                <Link href="/benefits">
                    <a className="bg-purple-500 text-white px-4 py-2 rounded">View Benefits</a>
                </Link>
            </div>
        </div>
    );
};

export default HomePage;