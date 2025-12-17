'use client'

import { useState } from 'react'
import { matchBenefits, type CitizenProfile, type BenefitMatch } from '../../lib/api'

export default function CitizenPage() {
  const [income, setIncome] = useState('')
  const [state, setState] = useState('')
  const [isStudent, setIsStudent] = useState(false)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<BenefitMatch[] | null>(null)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResults(null)

    const profile: CitizenProfile = {
      income: parseFloat(income),
      state,
      is_student: isStudent,
    }

    try {
      const response = await matchBenefits(profile)
      setResults(response.matched_benefits)
    } catch (err) {
      setError('Failed to check eligibility. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Check Your Eligibility</h1>

      <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="income" className="block text-sm font-medium text-gray-700 mb-2">
              Annual Family Income (INR)
            </label>
            <input
              type="number"
              id="income"
              value={income}
              onChange={(e) => setIncome(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="e.g., 350000"
              required
            />
          </div>

          <div>
            <label htmlFor="state" className="block text-sm font-medium text-gray-700 mb-2">
              State of Residence
            </label>
            <select
              id="state"
              value={state}
              onChange={(e) => setState(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              required
            >
              <option value="">Select your state</option>
              <option value="Karnataka">Karnataka</option>
              <option value="Maharashtra">Maharashtra</option>
              <option value="Tamil Nadu">Tamil Nadu</option>
              <option value="Kerala">Kerala</option>
              <option value="Andhra Pradesh">Andhra Pradesh</option>
              <option value="Telangana">Telangana</option>
              <option value="Gujarat">Gujarat</option>
              <option value="Rajasthan">Rajasthan</option>
              <option value="Punjab">Punjab</option>
              <option value="Haryana">Haryana</option>
            </select>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="isStudent"
              checked={isStudent}
              onChange={(e) => setIsStudent(e.target.checked)}
              className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <label htmlFor="isStudent" className="ml-2 block text-sm text-gray-700">
              I am currently a student
            </label>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 text-white py-3 px-6 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
          >
            {loading ? 'Checking Eligibility...' : 'Check Eligibility'}
          </button>
        </form>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-8">
          {error}
        </div>
      )}

      {results && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-gray-900">
            {results.length > 0 ? `Found ${results.length} Eligible Benefit(s)` : 'No Eligible Benefits Found'}
          </h2>

          {results.map((match, idx) => (
            <div key={idx} className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900">{match.policy.name}</h3>
                  {match.policy.description && (
                    <p className="text-gray-600 mt-1">{match.policy.description}</p>
                  )}
                </div>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                  ✓ Eligible
                </span>
              </div>

              {match.policy.benefits && (
                <div className="mb-4 p-3 bg-blue-50 rounded-md">
                  <p className="text-sm font-medium text-blue-900">Benefits:</p>
                  <p className="text-blue-700">{match.policy.benefits}</p>
                </div>
              )}

              <div className="border-t pt-4">
                <p className="text-sm font-medium text-gray-700 mb-2">Eligibility Check:</p>
                <div className="space-y-2">
                  {match.eligibility.reasons.map((reason, rIdx) => (
                    <div key={rIdx} className="flex items-start">
                      <span className={`mr-2 ${reason.satisfied ? 'text-green-600' : 'text-red-600'}`}>
                        {reason.satisfied ? '✓' : '✗'}
                      </span>
                      <span className="text-sm text-gray-700">{reason.message}</span>
                    </div>
                  ))}
                </div>
              </div>

              {match.application_guidance && (
                <div className="mt-4 p-3 bg-gray-50 rounded-md">
                  <p className="text-sm text-gray-700">{match.application_guidance}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
