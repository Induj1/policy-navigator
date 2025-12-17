'use client'

import Link from 'next/link'
import SystemStatus from '@/components/SystemStatus'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Welcome to Policy Navigator
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Multi-agent AI system for government policy interpretation, eligibility verification, and benefit matching
          </p>
          
          {/* System Status */}
          <div className="max-w-md mx-auto mb-12">
            <SystemStatus />
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <Link href="/citizen" className="block">
            <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow cursor-pointer">
              <div className="text-4xl mb-4">👤</div>
              <h2 className="text-2xl font-semibold text-gray-800 mb-3">Check Eligibility</h2>
              <p className="text-gray-600">
                Enter your details to find benefits you qualify for
              </p>
            </div>
          </Link>

          <Link href="/policies" className="block">
            <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow cursor-pointer">
              <div className="text-4xl mb-4">📋</div>
              <h2 className="text-2xl font-semibold text-gray-800 mb-3">Interpret Policies</h2>
              <p className="text-gray-600">
                Parse policy text and extract eligibility rules
              </p>
            </div>
          </Link>

          <Link href="/benefits" className="block">
            <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow cursor-pointer">
              <div className="text-4xl mb-4">🎁</div>
              <h2 className="text-2xl font-semibold text-gray-800 mb-3">View Benefits</h2>
              <p className="text-gray-600">
                Explore matched benefits and application guidance
              </p>
            </div>
          </Link>
        </div>

        <div className="mt-16 pt-8 border-t border-gray-200">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Powered by AI Agents</h3>
          <div className="flex flex-wrap justify-center gap-4 text-sm text-gray-600">
            <span className="bg-indigo-100 px-4 py-2 rounded-full">Policy Interpreter</span>
            <span className="bg-indigo-100 px-4 py-2 rounded-full">Eligibility Verifier</span>
            <span className="bg-indigo-100 px-4 py-2 rounded-full">Benefit Matcher</span>
            <span className="bg-indigo-100 px-4 py-2 rounded-full">Credential Issuer</span>
            <span className="bg-indigo-100 px-4 py-2 rounded-full">Advocacy Agent</span>
          </div>
        </div>
      </div>
    </div>
  )
}