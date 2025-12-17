'use client'

import { useState } from 'react'
import { interpretPolicy, getSamplePolicies, type Policy } from '../../lib/api'

export default function PoliciesPage() {
  const [policyText, setPolicyText] = useState('')
  const [policyName, setPolicyName] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Policy | null>(null)
  const [error, setError] = useState('')
  const [samplePolicies, setSamplePolicies] = useState<Policy[]>([])

  const loadSamplePolicies = async () => {
    try {
      const policies = await getSamplePolicies()
      setSamplePolicies(policies)
    } catch (err) {
      console.error('Failed to load sample policies:', err)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await interpretPolicy(policyText, policyName || undefined)
      setResult(response.policy)
    } catch (err) {
      setError('Failed to interpret policy. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const useSamplePolicy = (policy: Policy) => {
    setPolicyText(policy.raw_text)
    setPolicyName(policy.name)
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Interpret Policy Text</h1>

      <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="policyName" className="block text-sm font-medium text-gray-700 mb-2">
              Policy Name (Optional)
            </label>
            <input
              type="text"
              id="policyName"
              value={policyName}
              onChange={(e) => setPolicyName(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="e.g., Karnataka Education Scholarship"
            />
          </div>

          <div>
            <label htmlFor="policyText" className="block text-sm font-medium text-gray-700 mb-2">
              Policy Text
            </label>
            <textarea
              id="policyText"
              value={policyText}
              onChange={(e) => setPolicyText(e.target.value)}
              rows={8}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Paste policy text here. Example: The candidate must have annual family income below 800000 INR. The applicant must be a resident of Karnataka. The applicant must be enrolled as a full-time student."
              required
            />
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-indigo-600 text-white py-3 px-6 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
            >
              {loading ? 'Interpreting...' : 'Interpret Policy'}
            </button>
            <button
              type="button"
              onClick={loadSamplePolicies}
              className="bg-gray-200 text-gray-700 py-3 px-6 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 font-semibold"
            >
              Load Samples
            </button>
          </div>
        </form>
      </div>

      {samplePolicies.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Sample Policies</h2>
          <div className="space-y-3">
            {samplePolicies.map((policy, idx) => (
              <button
                key={idx}
                onClick={() => useSamplePolicy(policy)}
                className="w-full text-left p-4 border border-gray-200 rounded-md hover:bg-gray-50 transition-colors"
              >
                <p className="font-medium text-gray-900">{policy.name}</p>
                <p className="text-sm text-gray-600 mt-1 truncate">{policy.raw_text}</p>
              </button>
            ))}
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-8">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Extracted Rules</h2>

          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">{result.name}</h3>
            {result.description && (
              <p className="text-gray-600 mb-4">{result.description}</p>
            )}
          </div>

          <div className="border-t pt-6">
            <h4 className="text-md font-semibold text-gray-700 mb-4">Eligibility Rules ({result.rules.length})</h4>
            <div className="space-y-3">
              {result.rules.map((rule, idx) => (
                <div key={idx} className="flex items-center p-4 bg-gray-50 rounded-md">
                  <span className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded text-sm font-mono mr-4">
                    {idx + 1}
                  </span>
                  <div className="flex-1">
                    <code className="text-sm">
                      <span className="font-semibold text-gray-900">{rule.key}</span>
                      <span className="text-gray-600 mx-2">{rule.operator}</span>
                      <span className="text-indigo-600">
                        {typeof rule.value === 'boolean' ? rule.value.toString() : rule.value}
                      </span>
                    </code>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {result.benefits && (
            <div className="mt-6 p-4 bg-green-50 rounded-md">
              <p className="text-sm font-medium text-green-900">Benefits:</p>
              <p className="text-green-700">{result.benefits}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}