import React from 'react'
import type { Policy } from '../lib/api'

interface BenefitCardProps {
  policy: Policy
}

export default function BenefitCard({ policy }: BenefitCardProps) {
  return (
    <div className="border border-gray-200 rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow bg-white">
      <h3 className="text-xl font-bold text-gray-900 mb-2">{policy.name}</h3>
      
      {policy.description && (
        <p className="text-gray-600 mb-3">{policy.description}</p>
      )}
      
      {policy.benefits && (
        <div className="mb-4 p-3 bg-green-50 rounded-md">
          <p className="text-sm font-medium text-green-900">Benefits:</p>
          <p className="text-green-700">{policy.benefits}</p>
        </div>
      )}
      
      <h4 className="text-md font-semibold text-gray-800 mb-2">
        Eligibility Criteria ({policy.rules.length} requirements):
      </h4>
      <ul className="space-y-2">
        {policy.rules.map((rule, index) => (
          <li key={index} className="flex items-start text-sm">
            <span className="bg-indigo-100 text-indigo-800 px-2 py-1 rounded text-xs font-mono mr-2 mt-0.5">
              {index + 1}
            </span>
            <code className="text-gray-700">
              <span className="font-semibold">{rule.key}</span>
              <span className="text-gray-500 mx-1">{rule.operator}</span>
              <span className="text-indigo-600">
                {typeof rule.value === 'boolean' ? rule.value.toString() : rule.value}
              </span>
            </code>
          </li>
        ))}
      </ul>
    </div>
  )
}