import { useEffect, useState } from 'react';
import { Policy } from '../lib/types';
import { fetchPolicies } from '../lib/api';

const usePolicies = () => {
    const [policies, setPolicies] = useState<Policy[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadPolicies = async () => {
            try {
                const data = await fetchPolicies();
                setPolicies(data);
            } catch (err) {
                setError('Failed to load policies');
            } finally {
                setLoading(false);
            }
        };

        loadPolicies();
    }, []);

    return { policies, loading, error };
};

export default usePolicies;