'use client'

import { useEffect, useState } from 'react'
import { getSamplePolicies, type Policy } from '../../lib/api'
import PolicyCard from '../../components/PolicyCard'
import BenefitCard from '../../components/BenefitCard'

export default function BenefitsPage() {
  const [policies, setPolicies] = useState<Policy[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadPolicies()
  }, [])

  const loadPolicies = async () => {
    try {
      const data = await getSamplePolicies()
      setPolicies(data)
    } catch (err) {
      setError('Failed to load benefits. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">Available Benefits</h1>
      <p className="text-gray-600 mb-8">
        Explore government schemes and benefits. Go to{' '}
        <a href="/citizen" className="text-indigo-600 hover:underline">Check Eligibility</a>
        {' '}to find which ones you qualify for.
      </p>

      {loading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-gray-600">Loading benefits...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-8">
          {error}
        </div>
      )}

      {!loading && !error && (
        <div className="grid md:grid-cols-2 gap-6">
          {policies.map((policy, idx) => (
            <BenefitCard key={idx} policy={policy} />
          ))}
        </div>
      )}

      {!loading && !error && policies.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600">No benefits available at the moment.</p>
        </div>
      )}
    </div>
  )
}