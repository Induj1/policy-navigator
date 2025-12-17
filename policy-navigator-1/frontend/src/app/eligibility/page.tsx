import React, { useState } from 'react';
import { useEligibility } from '../../hooks/useEligibility';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';

const EligibilityPage = () => {
    const [income, setIncome] = useState('');
    const [state, setState] = useState('');
    const { checkEligibility, eligibilityResult } = useEligibility();

    const handleSubmit = (e) => {
        e.preventDefault();
        checkEligibility({ income, state });
    };

    return (
        <div className="eligibility-page">
            <h1>Check Your Eligibility</h1>
            <form onSubmit={handleSubmit}>
                <Input
                    type="number"
                    placeholder="Enter your income"
                    value={income}
                    onChange={(e) => setIncome(e.target.value)}
                />
                <Input
                    type="text"
                    placeholder="Enter your state"
                    value={state}
                    onChange={(e) => setState(e.target.value)}
                />
                <Button type="submit">Check Eligibility</Button>
            </form>
            {eligibilityResult && (
                <div className="eligibility-result">
                    <h2>Eligibility Result:</h2>
                    <p>{eligibilityResult}</p>
                </div>
            )}
        </div>
    );
};

export default EligibilityPage;