import React, { useState } from 'react';
import axios from 'axios';
import './ChatBox.css';

const ChatBox = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        if (input.trim() === '') return; // 防止发送空消息
        const response = await axios.post('http://localhost:5000/chat', { message: input });
        setMessages([...messages, { user: 'You', text: input }, { user: 'Bot', text: response.data.answer }]);
        setInput('');
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    };

    return (
        <div className="chatbox-container">
            <div className="messages-container">
                {messages.map((msg, index) => (
                    <div key={index}><strong>{msg.user}:</strong> {msg.text}</div>
                ))}
            </div>
            <div className="input-container">
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                />
                <button onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
};

export default ChatBox;
