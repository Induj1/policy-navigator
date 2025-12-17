'use client'

import { useEffect, useState } from 'react'

interface ZyndAIStatus {
  connected: boolean
  mode?: string
  registry_url?: string
  mqtt_broker?: string
  agent_did?: string
  identity_verified?: boolean
}

interface SystemStatusData {
  system: string
  version?: string
  zyndai: ZyndAIStatus
  features?: {
    policy_interpretation: boolean
    eligibility_checking: boolean
    benefit_matching: boolean
    credential_issuance: boolean
    agent_discovery: boolean
    encrypted_communication: boolean
  }
  error?: string
}

export default function SystemStatus() {
  const [status, setStatus] = useState<SystemStatusData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStatus()
    const interval = setInterval(fetchStatus, 30000) // Refresh every 30s
    return () => clearInterval(interval)
  }, [])

  const fetchStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/citizens/status')
      const data = await response.json()
      setStatus(data)
    } catch (error) {
      console.error('Failed to fetch status:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
        <div className="animate-pulse flex items-center">
          <div className="h-4 bg-gray-300 rounded w-32"></div>
        </div>
      </div>
    )
  }

  if (!status) return null

  const networkStatus = status.zyndai.connected ? 'Connected' : 'Offline'
  const networkColor = status.zyndai.connected ? 'text-green-600' : 'text-yellow-600'
  const dotColor = status.zyndai.connected ? 'bg-green-500' : 'bg-yellow-500'

  return (
    <div className="bg-white rounded-lg shadow-md p-4 border border-gray-200">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-800">System Status</h3>
        <button
          onClick={fetchStatus}
          className="text-sm text-blue-600 hover:text-blue-800"
          title="Refresh status"
        >
          ↻ Refresh
        </button>
      </div>

      {/* Network Status */}
      <div className="mb-4 p-3 bg-gray-50 rounded">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${dotColor} animate-pulse`}></div>
            <span className="font-medium text-gray-700">ZyndAI Network</span>
          </div>
          <span className={`font-semibold ${networkColor}`}>{networkStatus}</span>
        </div>
        
        {status.zyndai.connected && (
          <div className="mt-2 text-xs text-gray-600 space-y-1">
            {status.zyndai.mode && (
              <div>Mode: <span className="font-mono">{status.zyndai.mode}</span></div>
            )}
            {status.zyndai.registry_url && (
              <div>Registry: <span className="font-mono">{status.zyndai.registry_url}</span></div>
            )}
            {status.zyndai.agent_did && (
              <div>Agent DID: <span className="font-mono text-xs">{status.zyndai.agent_did.substring(0, 20)}...</span></div>
            )}
          </div>
        )}

        {!status.zyndai.connected && status.zyndai.mode && (
          <div className="mt-2 text-xs text-yellow-700 bg-yellow-50 p-2 rounded">
            Running in {status.zyndai.mode} mode - No network credentials configured
          </div>
        )}
      </div>

      {/* Features */}
      {status.features && (
        <div className="space-y-2">
          <h4 className="text-sm font-semibold text-gray-700">Features</h4>
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(status.features).map(([key, enabled]) => (
              <div key={key} className="flex items-center space-x-2 text-sm">
                <span className={enabled ? 'text-green-500' : 'text-gray-300'}>
                  {enabled ? '✓' : '○'}
                </span>
                <span className="text-gray-700 capitalize">
                  {key.replace(/_/g, ' ')}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {status.error && (
        <div className="mt-3 text-xs text-red-600 bg-red-50 p-2 rounded">
          Error: {status.error}
        </div>
      )}
    </div>
  )
}
