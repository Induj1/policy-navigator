import React, { useState } from 'react';
import { usePolicies } from '../../hooks/usePolicies';
import { PolicyCard } from '../../components/PolicyCard';

const PoliciesPage = () => {
    const [policyText, setPolicyText] = useState('');
    const { interpretPolicy, interpretedPolicies } = usePolicies();

    const handleSubmit = (e) => {
        e.preventDefault();
        interpretPolicy(policyText);
    };

    return (
        <div className="policies-page">
            <h1>Policy Interpretation</h1>
            <form onSubmit={handleSubmit}>
                <textarea
                    value={policyText}
                    onChange={(e) => setPolicyText(e.target.value)}
                    placeholder="Enter policy text here..."
                    rows={10}
                    className="textarea"
                />
                <button type="submit" className="submit-button">Interpret Policy</button>
            </form>
            <div className="interpreted-policies">
                {interpretedPolicies.map((policy, index) => (
                    <PolicyCard key={index} policy={policy} />
                ))}
            </div>
        </div>
    );
};

export default PoliciesPage;