import React from 'react';

interface PolicyCardProps {
    title: string;
    description: string;
    eligibilityCriteria: string;
    benefits: string[];
}

const PolicyCard: React.FC<PolicyCardProps> = ({ title, description, eligibilityCriteria, benefits }) => {
    return (
        <div className="bg-white shadow-md rounded-lg p-4">
            <h2 className="text-xl font-bold">{title}</h2>
            <p className="text-gray-700">{description}</p>
            <h3 className="text-lg font-semibold mt-2">Eligibility Criteria:</h3>
            <p className="text-gray-600">{eligibilityCriteria}</p>
            <h3 className="text-lg font-semibold mt-2">Benefits:</h3>
            <ul className="list-disc list-inside">
                {benefits.map((benefit, index) => (
                    <li key={index} className="text-gray-600">{benefit}</li>
                ))}
            </ul>
        </div>
    );
};

export default PolicyCard;