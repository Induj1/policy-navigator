import { useState, useEffect } from 'react';
import { fetchBenefits } from '../lib/api';
import { Benefit } from '../lib/types';

const useBenefits = () => {
    const [benefits, setBenefits] = useState<Benefit[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getBenefits = async () => {
            try {
                const data = await fetchBenefits();
                setBenefits(data);
            } catch (err) {
                setError('Failed to fetch benefits');
            } finally {
                setLoading(false);
            }
        };

        getBenefits();
    }, []);

    return { benefits, loading, error };
};

export default useBenefits;