import React from 'react';

interface PolicyCardProps {
  title: string;
  description: string;
  rules: Array<{ key: string; operator: string; value: any }>;
}

const PolicyCard: React.FC<PolicyCardProps> = ({ title, description, rules }) => {
  return (
    <div className="border rounded-lg p-4 shadow-md">
      <h2 className="text-xl font-bold">{title}</h2>
      <p className="text-gray-700">{description}</p>
      <h3 className="mt-2 font-semibold">Rules:</h3>
      <ul className="list-disc list-inside">
        {rules.map((rule, index) => (
          <li key={index}>
            {rule.key} {rule.operator} {rule.value}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PolicyCard;