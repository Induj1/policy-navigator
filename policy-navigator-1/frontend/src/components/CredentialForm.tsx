import React, { useState } from 'react';

const CredentialForm = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [income, setIncome] = useState('');
    const [state, setState] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        const credentials = {
            name,
            email,
            income,
            state,
        };
        // Call the API to submit the credentials
        console.log('Submitting credentials:', credentials);
    };

    return (
        <form onSubmit={handleSubmit} className="credential-form">
            <div>
                <label htmlFor="name">Name:</label>
                <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="email">Email:</label>
                <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="income">Income:</label>
                <input
                    type="number"
                    id="income"
                    value={income}
                    onChange={(e) => setIncome(e.target.value)}
                    required
                />
            </div>
            <div>
                <label htmlFor="state">State:</label>
                <input
                    type="text"
                    id="state"
                    value={state}
                    onChange={(e) => setState(e.target.value)}
                    required
                />
            </div>
            <button type="submit">Submit Credentials</button>
        </form>
    );
};

export default CredentialForm;