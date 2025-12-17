import React, { useEffect, useState } from 'react';
import { fetchBenefits } from '../../lib/api';
import BenefitList from '../../components/BenefitList';

const BenefitsPage = () => {
    const [benefits, setBenefits] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getBenefits = async () => {
            try {
                const data = await fetchBenefits();
                setBenefits(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        getBenefits();
    }, []);

    if (loading) {
        return <div>Loading benefits...</div>;
    }

    if (error) {
        return <div>Error fetching benefits: {error}</div>;
    }

    return (
        <div>
            <h1>Available Benefits</h1>
            <BenefitList benefits={benefits} />
        </div>
    );
};

export default BenefitsPage;