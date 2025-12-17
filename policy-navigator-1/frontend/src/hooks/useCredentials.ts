import { useState, useEffect } from 'react';
import { fetchCredentials } from '../lib/api';
import { Credential } from '../lib/types';

const useCredentials = () => {
    const [credentials, setCredentials] = useState<Credential[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadCredentials = async () => {
            try {
                const data = await fetchCredentials();
                setCredentials(data);
            } catch (err) {
                setError('Failed to load credentials');
            } finally {
                setLoading(false);
            }
        };

        loadCredentials();
    }, []);

    return { credentials, loading, error };
};

export default useCredentials;