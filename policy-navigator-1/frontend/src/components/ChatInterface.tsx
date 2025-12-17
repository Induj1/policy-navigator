import React, { useState } from 'react';

const ChatInterface: React.FC = () => {
    const [messages, setMessages] = useState<string[]>([]);
    const [input, setInput] = useState<string>('');

    const handleSend = () => {
        if (input.trim()) {
            setMessages([...messages, input]);
            setInput('');
            // Here you would typically send the input to the backend and get a response
            // For example: sendMessageToBackend(input).then(response => setMessages([...messages, response]));
        }
    };

    return (
        <div className="chat-interface">
            <div className="messages">
                {messages.map((msg, index) => (
                    <div key={index} className="message">
                        {msg}
                    </div>
                ))}
            </div>
            <div className="input-area">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                />
                <button onClick={handleSend}>Send</button>
            </div>
        </div>
    );
};

export default ChatInterface;